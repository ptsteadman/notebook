# CSS

#### Problem: Equal Height Columns

#### Problem: centering images

use display: block; margin-left: auto; margin-right: auto;
Bootstrap classes for this, and aligning text to the center
`center-block`

#### Absolute Centering of Item of Unknown Size

`margin-left: 50%;`
`transform: translateX(-50%);`

#### Problem: List Has Bullets
- Use `list-file-type: none;`

#### Horizontal Menus
- Use `display: inline-block;` instead of `float: left;` on the li

#### Z-Index With Fixed Elements
- `position: fixed;` elements have a different 'stacking context' than elements
  with other position values.  Therefore, zindexs aren't comparable.

#### Input Focus and Placeholder Styling

- to style the placeholder, use a bunch of vendor prefixes:

```
::-webkit-input-placeholder { /* WebKit, Blink, Edge */
  color:    $light-tan;
  opacity: 0.6;
}

:-moz-placeholder { /* Mozilla Firefox 4 to 18 */
  color:    $light-tan;
  opacity: 0.6;
}
::-moz-placeholder { /* Mozilla Firefox 19+ */
  color:    $light-tan;
  opacity: 0.6;
}
:-ms-input-placeholder { /* Internet Explorer 10-11 */
  color:    $light-tan;
}
```

For 'blue outline', use `input:focus { outline: 0 !important }`.  Don't do it to
all elements like buttons, it causes an accessability issue.

#### Problem: Centering inline-block Elements

Set `text-align: center;` on the parent.

#### Problem: Need body to fill viewport / sticky footer

```css

.Site {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.Site-content {
  flex: 1;
}

```


