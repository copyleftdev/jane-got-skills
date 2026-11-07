open! Core

module Side : sig
  type t =
    | Buy
    | Sell
  [@@deriving sexp, equal, quickcheck]
end

module Order : sig
  type t =
    { id : int
    ; side : Side.t
    ; price : int
    ; size : int
    }
  [@@deriving sexp]
end

module Fill : sig
  type t =
    { resting_id : int
    ; incoming_id : int
    ; price : int
    ; size : int
    }
  [@@deriving sexp]
end

(** Price-time priority: each side is sorted best price first, oldest first within a price. *)
type t [@@deriving sexp_of]

val empty : t
(** Best price first, oldest first within a price. *)
val orders : t -> Side.t -> Order.t list

val best_bid : t -> int option
val best_offer : t -> int option

(** Matches [order] against the opposite side, then rests any remainder. Raises if
    [order.size <= 0]. *)
val add : t -> Order.t -> t * Fill.t list

module For_testing : sig
  val total_size : t -> int
end
