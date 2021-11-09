const progressDone = document.querySelectorAll('.progress-done');
progressDone.forEach(progress => {
	progress.setAttribute("data-done","10");
});
const progress_percent = document.querySelectorAll('.percent');
progress_percent.forEach(percent => {
	percent.innerHTML="10.0";
});

update_progress();

function update_progress(){
	progressDone.forEach(progress => {
		progress.style.width = progress.getAttribute('data-done') + '%';
	});
}



// // SOCIAL PANEL JS
// const floating_btn = document.querySelector('.floating-btn');
// const close_btn = document.querySelector('.close-btn');
// const social_panel_container = document.querySelector('.social-panel-container');

// floating_btn.addEventListener('onchange', () => {
// 	social_panel_container.classList.toggle('visible')
// });

// close_btn.addEventListener('change', () => {
// 	social_panel_container.classList.remove('visible')
// });