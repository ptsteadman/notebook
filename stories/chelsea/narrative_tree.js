document.addEventListener('DOMContentLoaded', function(){
    console.log("hi");
    var rt = document.createElement('div');
    rt.class = 'text-node';
    rt.innerHTML = root['text'];
    var text = document.querySelector('#text');
    console.log(document.body);
    document.body.appendChild(rt);
});

