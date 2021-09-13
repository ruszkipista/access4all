//Responsive hamburger menu
$(document).ready(function () {
    $('.header-burger').click(function (event) {
        $('.header-burger, .header-menu').toggleClass('active');
        $('body').toggleClass('lock')
    });
    $(".copyright").text(new Date().getFullYear())
});

AOS.init();

// Interviews page - delete confirmation modal
document.addEventListener('DOMContentLoaded', connectModal());

function connectModal() {
    const sources = document.querySelectorAll('a[data-bs-toggle="modal"]');
    sources.forEach(source => {
        source.addEventListener("click", event => {
            // extract target modal from attribute data-target
            const targetModal = document.querySelector(source.dataset.bsTarget);
            if (targetModal) {
                // get the Button element with data-form-method attribute
                const targetButton = targetModal.querySelector('button[data-form-method]');
                targetButton.formAction = source.href;
                targetButton.addEventListener('click', (event) => {
                    fetch(event.target.formAction, {method:event.target.dataset.formMethod})
                    // learnt handling the returned whole page here https://gomakethings.com/getting-html-with-fetch-in-vanilla-js/
                    .then(result=> result.text())
                    .then(html => document.querySelector('html').innerHTML = html)
                    .then(_ => connectModal()); 
                });
            }
        });
    });
}
