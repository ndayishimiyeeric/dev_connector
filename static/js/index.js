const searchForm = document.getElementById('searchForm')
const linkBtn = document.querySelectorAll('.link_btn')
const ulDefaultTab = document.getElementById('defaultTab')

if (ulDefaultTab) {
    // check if one of the li aria-selected is true
    let liSelected = ulDefaultTab.querySelector('[aria-selected="true"]')

    linkBtn.forEach((btn) => {
        btn.addEventListener(('click'), (e) => {
            e.preventDefault()
            console.log('clicked', liSelected)
        })
    })
}


if (searchForm) {
    linkBtn.forEach((btn) => {
        btn.addEventListener('click',  (e) => {
            e.preventDefault()

            let page = btn.getAttribute('data-page')
            searchForm.innerHTML += `<input value=${page} name="page" hidden />`
            searchForm.submit()


        })
    })
}

let themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
let themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

let themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function() {

    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }

});
