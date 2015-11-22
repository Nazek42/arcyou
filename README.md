# Arcyóu
A LISP-like functional programming language suitable for code golf

#### Atoms
An atom in Arcyóu is a *numeric literal* like `3.14`, a *string literal* like `"foobar"`, or a *variable reference* like `my-variable`.

Literals evaluate to themselves. Variables evaluate to their value.

*Note: string literals adjacent to other atoms __must__ be separated by spaces. Example:* `x "foobar" 2`, *not* `x"foobar"2`.

#### Cells
A cell is a combination of one or more atoms in parentheses, like so:

    (p "Hello, World!" 8 super-special-string)

A cell can either be a *function call* or a *special form*. A special form is a cell where the first atom is one of the following:

 - `?`
 - `@`
 - `f`
 - `:`
 - `F`
 - `'`

If the first atom is anything else, the cell is a function call.

###### Function Calls

Function calls are of the form `(func arg1 arg2 arg3 ...)`. Where most languages would have built-in operators for things like addition and subtraction, Arcyóu has built-in functions. For example:

    (+ 1 2) --> 3
    (= 2 3) --> False
    (_ 2 5) --> [2, 3, 4]
    (* 5 4 3 2) --> 120

This means that you can redefine things like `+` or `_` to be *whatever you want*. Use this power wisely!

###### Special Forms

The other type of cell is a *special form*. These are things that are necessary in the language, but don't quite conform to the syntax rules of a function call. There are six special forms in Arcyóu.

Atom | Meaning | Syntax | Example
-----|---------|--------|--------
`?`|If statement|`(? condition if-true if-false)`|`(? (= x 3) "x is 3" "x is not 3")`
`@`|While loop|`(@ condition loop-body)`|`(@ (< x 6) (p (+ x 1)))`
`f`|For loop|`(f variable iterable loop-body)`|`(f n my-list (p n))`
`:`|Set variable|`(: symbol value)`|`(: my-number -7.2)`
`F`|Anonymous function|`(F (arguments) (function-body))`|`(F (x y) (+ x y))`
`'`|Quote|`(' anything)`|`(' 1 2 3 4)`
