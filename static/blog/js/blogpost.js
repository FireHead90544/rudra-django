let modal = document.getElementById("commentDeleteModal");
let close_button = document.getElementById("closeCommentModal");

let addReplies = Array.from(document.getElementsByClassName("addReplies"));
let viewReplies = Array.from(document.getElementsByClassName("viewReplies"));

close_button.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

let comments = Array.from(document.getElementsByClassName("delete-comment"));
comments.forEach((comment) => {
    comment.addEventListener("click", function () {
        deleteComment(comment.getAttribute("trigger-target"));
    });
});

function deleteComment(comment_id) {
    modal.querySelector("#commentSno").value = comment_id;
    modal.style.display = "flex";
}

addReplies.forEach((addReply) => {
    addReply.addEventListener("click", function () {
        this.nextElementSibling.classList.toggle("hidden");
        this.remove()
    });
});

viewReplies.forEach((viewReply) => {
    viewReply.addEventListener("click", function () {
        this.nextElementSibling.classList.toggle('hidden');
    });
});