// const likeButton = document.getElementById('like-post');
// likeButton.addEventListener('click', e => {
//     e.preventDefault();
//     const url = '/<int:pk>/like/'; // Replace <int:pk> with the actual value of the primary key
//     const data = new URLSearchParams();
//     data.append('post_pk', '{{object.pk}}');
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
//             'X-CSRFToken': '{{ csrf_token }}'
//         },
//         body: data
//     })
//     .then(response => response.json())
//     .then(response => {
//         const counter = document.getElementById('like_count');
//         counter.textContent = response.like_count + '件のいいね';
//         const icon = document.getElementById('icon');
//         if (response.method === 'create') {
//             icon.classList.remove('far');
//             icon.classList.add('fas');
//             icon.id = 'icon';
//         } else {
//             icon.classList.remove('fas');
//             icon.classList.add('far');
//             icon.id = 'icon';
//         }
//     })
//     .catch(error => {
//         console.log('Request failed. Error:', error);
//     });
// });
