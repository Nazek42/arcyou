(: P 3.1415926535897932384626433832795028841971694)
(: T (* 2 P))
(: mE 2.7182818284590452353602874713527)

(: p? (F(x)
  (? (< x 2)
    n
    (& (f i (_ 2 x)
      (% x i))))))

(: d/ (F(x)
  (/ (F(i) (‰ x i)) (_ 1 (] x)))))

(: f! (F(x)
  (r * (_ 2 (] x)))))

(: d? ‰)
