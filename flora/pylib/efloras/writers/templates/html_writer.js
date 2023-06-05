document.querySelector('tbody')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const taxonId = event.target.dataset.taxonId;
        const selector = `[data-taxon-id="${taxonId}"]`;
        const elts = document.querySelectorAll(selector);
        elts.forEach(function(tr) {  tr.classList.toggle('closed'); });
    });
