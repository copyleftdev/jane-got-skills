open! Core
open Expect_test_helpers_core

let order id side ~price ~size = { Book.Order.id; side; price; size }

let show_add book o =
  let book, fills = Book.add book o in
  print_s [%sexp { fills : Book.Fill.t list; book : Book.t }];
  book
;;

let print_ladder book =
  let line (o : Book.Order.t) = printf "  %-4s %d x %d  #%d\n" (Sexp.to_string [%sexp (o.side : Book.Side.t)]) o.price o.size o.id in
  List.iter (List.rev (Book.orders book Sell)) ~f:line;
  print_endline "  ----";
  List.iter (Book.orders book Buy) ~f:line
;;

let step book o =
  let book, fills = Book.add book o in
  List.iter fills ~f:(fun f ->
    printf "fill #%d vs #%d: %d @ %d\n" f.incoming_id f.resting_id f.size f.price);
  print_ladder book;
  book
;;

let%expect_test "an order that does not cross rests on the book" =
  let book = show_add Book.empty (order 1 Buy ~price:100 ~size:5) in
  [%expect {|
    ((fills ())
     (book (
       (buys ((
         (id    1)
         (side  Buy)
         (price 100)
         (size  5))))
       (sells ()))))
    |}];
  let (_ : Book.t) = show_add book (order 2 Sell ~price:101 ~size:3) in
  [%expect {|
    ((fills ())
     (book (
       (buys ((
         (id    1)
         (side  Buy)
         (price 100)
         (size  5))))
       (sells ((
         (id    2)
         (side  Sell)
         (price 101)
         (size  3)))))))
    |}]
;;

let%expect_test "a crossing order fills at the resting price, oldest first" =
  let book =
    List.fold
      [ order 1 Sell ~price:101 ~size:2; order 2 Sell ~price:101 ~size:2; order 3 Sell ~price:102 ~size:5 ]
      ~init:Book.empty
      ~f:(fun book o -> fst (Book.add book o))
  in
  print_ladder book;
  [%expect {|
    Sell 102 x 5  #3
    Sell 101 x 2  #2
    Sell 101 x 2  #1
    ----
    |}];
  let (_ : Book.t) = step book (order 4 Buy ~price:102 ~size:5) in
  [%expect {|
    fill #4 vs #1: 2 @ 101
    fill #4 vs #2: 2 @ 101
    fill #4 vs #3: 1 @ 102
      Sell 102 x 4  #3
      ----
    |}]
;;

let%expect_test "best bid and offer, as a table" =
  let steps =
    [ order 1 Buy ~price:99 ~size:1
    ; order 2 Buy ~price:100 ~size:1
    ; order 3 Sell ~price:102 ~size:1
    ; order 4 Sell ~price:100 ~size:1
    ; order 5 Sell ~price:101 ~size:1
    ]
  in
  let show = Option.value_map ~default:"-" ~f:Int.to_string in
  printf "%-3s %-5s %-5s %4s %5s\n" "id" "side" "price" "bid" "offer";
  ignore
    (List.fold steps ~init:Book.empty ~f:(fun book (o : Book.Order.t) ->
       let book, _ = Book.add book o in
       printf
         "%-3d %-5s %-5d %4s %5s\n"
         o.id
         (Sexp.to_string [%sexp (o.side : Book.Side.t)])
         o.price
         (show (Book.best_bid book))
         (show (Book.best_offer book));
       book)
     : Book.t);
  [%expect {|
    id  side  price  bid offer
    1   Buy   99      99     -
    2   Buy   100    100     -
    3   Sell  102    100   102
    4   Sell  100     99   102
    5   Sell  101     99   101
    |}]
;;

let%expect_test "a non-positive size is rejected" =
  require_does_raise [%here] (fun () -> Book.add Book.empty (order 1 Buy ~price:100 ~size:0));
  [%expect {|
    ("order size must be positive" (
      order (
        (id    1)
        (side  Buy)
        (price 100)
        (size  0))))
    |}]
;;

let order_generator =
  let open Base_quickcheck.Generator.Let_syntax in
  let%map id = Base_quickcheck.Generator.int_inclusive 1 1000
  and side = Book.Side.quickcheck_generator
  and price = Base_quickcheck.Generator.int_inclusive 95 105
  and size = Base_quickcheck.Generator.int_inclusive 1 10 in
  { Book.Order.id; side; price; size }
;;

let%expect_test "matching conserves size and never leaves the book crossed" =
  Base_quickcheck.Test.run_exn
    (module struct
      type t = Book.Order.t list [@@deriving sexp_of]

      let quickcheck_generator = Base_quickcheck.Generator.list order_generator
      let quickcheck_shrinker = Base_quickcheck.Shrinker.list Base_quickcheck.Shrinker.atomic
    end)
    ~f:(fun orders ->
      let book, filled =
        List.fold orders ~init:(Book.empty, 0) ~f:(fun (book, filled) o ->
          let book, fills = Book.add book o in
          book, filled + List.sum (module Int) fills ~f:(fun f -> f.size))
      in
      let added = List.sum (module Int) orders ~f:(fun o -> o.size) in
      [%test_result: int] (Book.For_testing.total_size book + (2 * filled)) ~expect:added;
      match Book.best_bid book, Book.best_offer book with
      | Some bid, Some offer -> assert (bid < offer)
      | _ -> ());
  [%expect {||}]
;;

let stamp msg = printf "%s %s\n" (Time_ns.to_string_utc (Time_ns.now ())) msg

let%expect_test "censor what is not deterministic before it reaches the block" =
  stamp "book opened";
  let censor = String.map ~f:(fun c -> if Char.is_digit c then 'X' else c) in
  print_string (censor [%expect.output]);
  [%expect {| XXXX-XX-XX XX:XX:XX.XXXXXXXXXZ book opened |}]
;;
