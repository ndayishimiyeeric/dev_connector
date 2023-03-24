const searchForm = document.getElementById('searchForm')
const linkBtn = document.querySelectorAll('.link_btn')


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
