const playlistTab = document.getElementById('playlists_tab')
const playlistTabContent = document.getElementById('playlists_tab_content')

const deleteFromPlaylist = (movie, uid) => {
    const url = `/api/playlist/${uid}/`
    data = { item_id: movie.id, media_type: movie.media_type }

    fetch(url, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then((res) => console.log(res))
    .then(() => {
        const rowDeleted = document.querySelector(`[data-id="${movie.id}"][data-media-type="${movie.media_type}"]`)
        rowDeleted.parentNode.removeChild(rowDeleted)
    })
    .catch((err) => console.log(err))
}

const deletePlaylist = (uid, title) => {
    const url = `/api/playlists/${uid}/delete/`
    fetch(url, { method: 'POST' })
    .then(() => {
        const plTab = document.getElementById(title.replace(/\s/g, '_'))
        const plContent = document.getElementById(`${title.replace(/\s/g, '_')}-tab`)

        plTab.parentNode.removeChild(plTab)
        plContent.parentNode.removeChild(plContent)
    })
    .catch(err => console.error(err))
}

const renderMovie = (movie, uid) => {
    console.log(movie)
    const posterCol = document.createElement('td')

    if(movie.poster_path !== null) {
        posterCol.innerHTML = `<img class='poster' alt="${movie.title || movie.name}" src="https://image.tmdb.org/t/p/w200${movie.poster_path}" />`
    } else {
        posterCol.innerHTML = `<img class='poster' src="null" alt='No Image' />`
    }

    const titleCol = document.createElement('td')
    titleCol.innerHTML = `<h5 class="row_title">${movie.title || movie.name}</h5>`

    const mediaTypeCol = document.createElement('td')
    mediaTypeCol.textContent = movie.media_type == 'movie' ? 'Movie': 'Tv Show'

    const releaseDateCol = document.createElement('td')
    releaseDateCol.className = 'no_break'
    releaseDateCol.textContent = movie.release_date || movie.first_air_date

    const voteCol = document.createElement('td')
    voteCol.textContent = movie.vote_average

    const detailBtnCol = document.createElement('td')
    detailBtnCol.innerHTML = `<a class="btn btn-info" href="#">Details</a>`

    const addToBtnCol = document.createElement('td')
    addToBtnCol.className = 'btn_row'
    const addToBtn = document.createElement('button')
    addToBtn.textContent = 'Add To'
    addToBtn.className = 'btn btn-primary'

    addToBtnCol.appendChild(addToBtn)

    const deleteCol = document.createElement('td')
    deleteCol.className = 'btn_row'
    const deleteBtn = document.createElement('button')
    deleteBtn.textContent = 'Remove'
    deleteBtn.className = 'btn btn-danger'
    deleteCol.appendChild(deleteBtn)

    deleteBtn.addEventListener('click', () => {
        deleteFromPlaylist(movie, uid)
    })

    const row = document.createElement('tr')
    row.setAttribute('data-id', movie.id)
    row.setAttribute('data-media-type', movie.media_type)

    row.appendChild(posterCol)
    row.appendChild(titleCol)
    row.appendChild(mediaTypeCol)
    row.appendChild(releaseDateCol)
    row.appendChild(voteCol)
    row.appendChild(detailBtnCol)
    row.appendChild(addToBtnCol)
    row.appendChild(deleteCol)

    return row
}

const renderDeletPlaylistBtn = (uid, title) => {
    const btnDel = document.createElement('button')
    btnDel.className = 'btn btn-danger mx-auto'
    btnDel.textContent = 'Delete Playlist'

    btnDel.addEventListener('click', () => {
        deletePlaylist(uid, title)
    })

    const editBtn = document.createElement('a')
    editBtn.textContent = 'edit playlist'
    editBtn.href = `/playlists/${uid}/edit/`
    editBtn.className = 'btn btn-warning mx-3'

    const btnDiv = document.createElement('div')
    btnDiv.className = 'col-12 my-3'
    btnDiv.appendChild(btnDel)
    btnDiv.appendChild(editBtn)

    return btnDiv
}


const renderTab = (title) => {
    const anchorTab = document.createElement('a')
    anchorTab.className = 'nav-link'
    anchorTab.setAttribute('data-toggle', 'tab')
    anchorTab.href = `#${title.replace(/\s/g, '_')}`
    anchorTab.textContent = title
    anchorTab.id = `${title.replace(/\s/g, '_')}-tab`

    return anchorTab
}

const renderTabContent = (title, list, uid) => {
    const tbody = document.createElement('tbody')
    list.forEach(movie => {
        tbody.appendChild(renderMovie(movie, uid))
    })

    const tableHead = `<thead>
            <tr>
                <th scope="col">Poster</th>
                <th scope="col">Title</th>
                <th scope="col">Media Type</th>
                <th scope="col">Release Date</th>
                <th scope="col">Vote</th>
                <th scope="col"></th>
                <th scope="col"></th>
                <th scope="col"></th>
            </tr>
        </thead>`

    const table = document.createElement('table')
    table.className = 'table table-light'
    table.innerHTML += tableHead
    table.appendChild(tbody)

    const contentDiv = document.createElement('div')
    contentDiv.className = 'tab-pane'
    contentDiv.id = title.replace(/\s/g, '_')

    contentDiv.appendChild(table)
    contentDiv.appendChild(renderDeletPlaylistBtn(uid, title))

    return contentDiv
} 

const renderPlaylist = (playlist) => {
    const title = playlist.title
    const uid = playlist.id
    const mediaList = playlist.items

    playlistTab.appendChild(renderTab(title))
    playlistTabContent.appendChild(renderTabContent(title, mediaList, uid))
}

const setupUI = (list) => {
    playlistTab.innerHTML = ''
    playlistTabContent.innerHTML = ''

    list.forEach(playlist => {
        renderPlaylist(playlist)
    })

    const firstTab = document.getElementById(list[0].title.replace(/\s/g, '_') + '-tab')
    const firstPanel = document.getElementById(list[0].title.replace(/\s/g, '_'))

    firstTab.classList.add('active')
    firstTab.setAttribute('aria-selected', 'true')
    firstPanel.classList.add('show')
    firstPanel.classList.add('active')
}

const getPlaylists = async () => {
    const response = fetch('/api/playlists/')
    const data = (await response).json()

    return data
}

addEventListener('DOMContentLoaded', async () => {
    const playlists = await getPlaylists()
    setupUI(playlists)
})