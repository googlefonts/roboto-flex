# Roboto Extremo Animations

This page contains simple demos to demonstrate Roboto Extremo's variable axes.

## Notes

Of all five registered axes, `wght` is the only one that can be reliably animated through its standard attribute `font-weight`:

```CSS
@keyframes weight-animation {
	from { font-weight: 100;  }
	to   { font-weight: 1000; }
}
```

The `wdth` axis can be set through `font-stretch`, but CSS animations [can't be used to animate the value in Chrome](https://bugs.chromium.org/p/chromium/issues/detail?id=924353). As a workaround, we're setting the `wdth` axis through `font-variation-settings`. Since CSS variables (a.k.a. custom properties) [can't be animated](https://www.w3.org/TR/css-variables-1/#defining-variables) we can't do the following:

```CSS
@keyframes width-animation {
	from { --wdth: 25; }
	to   { --wdth: 151; }
}
```

Instead, we have to animate the axis directly:

```CSS
@keyframes width-animation {
	from { 	font-variation-settings: 'wdth'  25, 'slnt' var(--slnt), 'GRAD' var(--GRAD); }
	to   { 	font-variation-settings: 'wdth' 151, 'slnt' var(--slnt), 'GRAD' var(--GRAD); }
}
```