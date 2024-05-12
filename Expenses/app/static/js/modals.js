// Funzione di utilità per mostrare o nascondere i modali
function toggleModal(modalId, show) {
    var modal = document.getElementById(modalId);
    modal.style.display = show ? 'block' : 'none';
}

// Event listener per chiudere i modali quando si clicca fuori o si preme 'Esc'
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        toggleModal(event.target.id, false);
    }
};
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        var modals = document.getElementsByClassName('modal');
        Array.from(modals).forEach(function(modal) {
            toggleModal(modal.id, false);
        });
    }
});
// Event listener per chiudere i modali quando si clicca sul pulsante di chiusura
var closeButtons = document.getElementsByClassName('close');
Array.from(closeButtons).forEach(function(button) {
    button.onclick = function() {
        var modal = button.closest('.modal');
        toggleModal(modal.id, false);
    };
});