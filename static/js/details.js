const btnAddTo = document.getElementById('add_to_btn')
const playlistModel = document.getElementById('playlists_model_body')

const addMovieToPlaylist = (playlist, movie) => {
    const url = `/api/playlist/add/${playlist.uid}/`
    const data = {'item_id': movie.id, 'media_type': movie.media_type}

    fetch(url, { method: 'POST', body: JSON.stringify(data)})
    .then(() => {
        const closeBtn = document.getElementById('close_model')
        closeBtn.click()
    }).catch(err => console.log(err))
}

const renderPlaylistBtn = (playlist, movie) => {
    const btn = document.createElement('button')
    btn.className = 'btn btn-info'
    btn.textContent = `add to ${playlist.title}`

    btn.addEventListener('click', () => {
        addMovieToPlaylist(playlist, movie)
    })

    const btnDiv = document.createElement('div')
    btnDiv.className = 'row my-1 px-2'
    btnDiv.appendChild(btn)

    return btnDiv
}

const renderCreatePlBtn = () => {
    const btn = document.createElement('a')
    btn.className = 'btn btn-secondary'
    btn.textContent = 'Create new playlist'
    btn.href = '/playlists/add/'

    const btnDiv = document.createElement('div')
    btnDiv.className = 'row my-1 px-2'
    btnDiv.appendChild(btn)

    return btnDiv
}

const showPlaylists = (movie) => {
    fetch('/api/playlists_lite/')
    .then(res => res.json())
    .then(data => {
        playlistModel.innerHTML = ''
        data.forEach(playlist => {
            playlistModel.appendChild(renderPlaylistBtn(playlist, movie))
        })
        
        playlistModel.appendChild(renderCreatePlBtn())
    })
    .catch(err => console.log(err))
}

btnAddTo.addEventListener('click', () => {
    showPlaylists(media)
})