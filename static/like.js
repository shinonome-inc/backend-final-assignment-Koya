// document.querySelectorAll('.like-button').forEach(function(button) {
//     button.addEventListener('click', function() {
//         var tweetId = this.dataset.tweetId;
//         var xhr = new XMLHttpRequest();
//         xhr.open('POST', '/tweets/' + tweetId + '/like/');
//         xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
//         xhr.onload = function() {
//             if (xhr.status === 200) {
//                 alert('いいねしました');
//             }
//         };
//         xhr.send();
//     });
// });

// document.querySelectorAll('.like-button').forEach(function(button) {
//     button.addEventListener('click', function() {
//         var tweetId = this.dataset.tweetId;
//         var isLiked = this.dataset.isLiked === 'true';
//         var xhr = new XMLHttpRequest();
//         var url = '/tweets/' + tweetId + (isLiked ? '/unlike/' : '/like/');
//         xhr.open('POST', url);
//         xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
//         xhr.onload = function() {
//             if (xhr.status === 200) {
//                 isLiked = !isLiked;
//                 button.dataset.isLiked = isLiked;
//                 button.style.color = isLiked ? 'red' : 'black';
//             }
//         };
//         xhr.send();
//     });
// });
