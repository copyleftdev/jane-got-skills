open! Core

module Side = struct
  type t =
    | Buy
    | Sell
  [@@deriving sexp, equal, quickcheck]
end

module Order = struct
  type t =
    { id : int
    ; side : Side.t
    ; price : int
    ; size : int
    }
  [@@deriving sexp]
end

module Fill = struct
  type t =
    { resting_id : int
    ; incoming_id : int
    ; price : int
    ; size : int
    }
  [@@deriving sexp]
end

type t =
  { buys : Order.t list
  ; sells : Order.t list
  }
[@@deriving sexp]

let empty = { buys = []; sells = [] }

let orders t (side : Side.t) =
  match side with
  | Buy -> t.buys
  | Sell -> t.sells
;;

let best_bid t = List.hd t.buys |> Option.map ~f:(fun (o : Order.t) -> o.price)
let best_offer t = List.hd t.sells |> Option.map ~f:(fun (o : Order.t) -> o.price)

let crosses (incoming : Order.t) (resting : Order.t) =
  match incoming.side with
  | Buy -> incoming.price >= resting.price
  | Sell -> incoming.price <= resting.price
;;

let better_or_equal side a b =
  match (side : Side.t) with
  | Buy -> a >= b
  | Sell -> a <= b
;;

let rest (order : Order.t) queue =
  let ahead, behind =
    List.split_while queue ~f:(fun (o : Order.t) ->
      better_or_equal order.side o.price order.price)
  in
  ahead @ (order :: behind)
;;

let add t (order : Order.t) =
  if order.size <= 0 then raise_s [%message "order size must be positive" (order : Order.t)];
  let rec match_against (incoming : Order.t) opposite fills =
    match opposite with
    | resting :: others when incoming.size > 0 && crosses incoming resting ->
      let size = Int.min incoming.size resting.size in
      let fill =
        { Fill.resting_id = resting.id; incoming_id = incoming.id; price = resting.price; size }
      in
      let incoming = { incoming with size = incoming.size - size } in
      let opposite =
        if resting.size = size then others else { resting with size = resting.size - size } :: others
      in
      match_against incoming opposite (fill :: fills)
    | _ -> incoming, opposite, List.rev fills
  in
  let same, opposite =
    match order.side with
    | Buy -> t.buys, t.sells
    | Sell -> t.sells, t.buys
  in
  let remaining, opposite, fills = match_against order opposite [] in
  let same = if remaining.size > 0 then rest remaining same else same in
  let t =
    match order.side with
    | Buy -> { buys = same; sells = opposite }
    | Sell -> { buys = opposite; sells = same }
  in
  t, fills
;;

module For_testing = struct
  let total_size t =
    List.sum (module Int) (t.buys @ t.sells) ~f:(fun (o : Order.t) -> o.size)
  ;;
end
