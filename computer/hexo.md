# Hexo Notes

### Setup

To Update NPM: `npm install npm@latest -g`.

In 2015 it makes sense to use NVM.  [NVM Installation Instructions](http://linoxide.com/ubuntu-how-to/install-node-js-ubuntu)

Hexo: why can't you use helper functions in source code? 
Should be in docs.

### Creating a Custom Index File in Hexo

Trying to generate a custom index file in source, hexo would ignore
`source/index.md` no matter what I did.  What I had to do was uninstall
`hexo-generator-index`.  [See
here.](https://github.com/hexojs/hexo/issues/1077).  Then it works.  So, that
will be part of the setup for my theme.  But, it's worth it in order to properly
seperate the theme from the content, I think.  Having everyone edit the theme
index.ejs template is no good.


### Hexo Rendering Raw EJS File Problem I Encountered

Sometimes the server would keep rendering an old version of my code, but as
text.  So I'd see stuff like

<% if (site.tags.length){ %>

The raw ejs, essentially.  Restarting the server or running `hexo clean` didn't
do anything.

After some time, I realized it was due to the gedit swap files being read by
hexo as the actual layout files: for example, `tag.ejs~`.  My `partial` helpers
looked like: `<%- partial('_partials/tag') %>`, and apparently hexo was reading
in `tag.ejs~` instead of `tag.ejs`.  And therefore, the ejs wasn't rendering.

To fix this, I simply changed my partial helper to `<%-
partial('_partials/tag.ejs') %>`.  Problem solved.

### Hexo Excerpt Variable

I was confused by the behavior of the hexo `excerpt` variable.  If you define
`excerpt: something` in the front matter, hexo ignores that.  Instead, to get it
to work, one needs to add a `<!-- more -->` comment in the source of the post.
Or, you can install a plugin that allows you to define custom excerpt in the
front matter.
