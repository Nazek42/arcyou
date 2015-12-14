; Copyright 2015 Benjamin Kulas
;
; This file is part of Arcyóu.
;
; Arcyóu is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; Arcyóu is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with Arcyóu, located in the file `LICENSE'. If not, see
; <http://www.gnu.org/licenses/>.


(: P 3.1415926535897932384626433832795028841971694) ; Pi
(: T (* 2 P)) ; Tau aka 2pi
(: mE 2.7182818284590452353602874713527) ; e

; Primality test
(: p? (F(x)
  (? (< x 2)
    n
    (& (f i (_ 2 x)
      (% x i))))))

; Divisor list
(: d/ (F(x)
  (/ (F(i) (‰ x i)) (_ 1 (] x)))))

; Factorial
(: f! (F(x)
  (r * (_ 2 (] x)))))

; Random choice
(: c (F(L)
  (L (# (* (R) (_ L))))))

; Random integer
(: r# (F(a b)
  (c (_ a b))))
