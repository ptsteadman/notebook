To Update NPM: npm install npm@latest -g
NVM Installation Instructions:
http://linoxide.com/ubuntu-how-to/install-node-js-ubuntu/

Hexo: why can't you use helper functions in source code? 
Should be in docs.

Trying to generate a custom index file in source, hexo would ignore
`source/index.md` no matter what I did.  What I had to do was uninstall
`hexo-generator-index`.  [See
here.](https://github.com/hexojs/hexo/issues/1077).  Then it works.  So, that
will be part of the setup for my theme.  But, it's worth it in order to properly
seperate the theme from the content, I think.  Having everyone edit the theme
index.ejs template is no good.



