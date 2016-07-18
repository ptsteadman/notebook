# Webpack Notes

`react-three-renderer` is a much better library, mostly because of the excellent
examples.

### Webpack General

Webpack doesn't throw an error when you don't have a loader installed?

### Webpack Dev Server vs Build

The index.html document can be loaded using `require('file?name=[name].[ext]!../index.html');`,
and will be served at `/`, (based on the name=) query, and thus served by webpack dev server here.

Passing the `-d` flag provides source maps.

### Loading Fonts/Images/Etc With Webpack 

The assets must first be loaded in the webpack config.  This looks like:

```
loaders: [
   ...,
  { test: /\.(ttf|otf|eot|svg|woff(2)?)$/,
    exclude: /node_modules/,
    loader: 'file?name=dist/fonts/[name].[ext]'
  } 
]

```
