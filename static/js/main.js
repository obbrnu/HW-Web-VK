function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const items = document.getElementsByClassName("counterOfLikes")

for (let item of items) {
    console.log(item.dataset.id);
    const [counter, buttonLike, buttonDislike] = item.children;
    buttonLike.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('question_id', item.dataset.id)

        const request = new Request('/likes/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.key;
            });
    })

    buttonDislike.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('question_id', item.dataset.id)

        const request = new Request('/dislikes/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.key;
            });
    })
}