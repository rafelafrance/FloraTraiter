document.querySelector('thead')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const cls = event.target.classList;
        const trs = document.querySelectorAll('tr.term');
        const buttons = document.querySelectorAll('button.toggle');
        if (cls.contains('closed')) {
            trs.forEach(function(tr) {  tr.classList.remove('closed'); });
            buttons.forEach(function(b) {  b.classList.remove('closed'); });
        } else {
            trs.forEach(function(tr) {  tr.classList.add('closed'); });
            buttons.forEach(function(b) {  b.classList.add('closed'); });
        }
 });
