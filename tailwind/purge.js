// Just removes all the comments from the build.min.css to reduce the file size furthermore
// Specifically made to remove the "/*! tailwindcss v3.2.7 | MIT License | https://tailwindcss.com*/"

var fs = require('fs');

fs.readFile('../static/build.min.css', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  var result = data.replace(/\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$/gm, '');
  fs.writeFile('../static/build.min.css', result, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});