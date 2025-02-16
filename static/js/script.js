// let selectedMultiplier = 0.1; // Default multiplier

//     document.querySelectorAll("#petrol-list li").forEach(li => {
//         li.addEventListener("click", function () {
//             // Barcha `li` larni oddiy holatga qaytarish
//             document.querySelectorAll("#petrol-list li").forEach(item => item.style.fontWeight = "normal");
            
//             // Tanlangan `li` ni ajratib ko'rsatish
//             this.style.fontWeight = "bold"; 
            
//             // Multiplikatorni o'zgartirish
//             selectedMultiplier = parseFloat(this.getAttribute("data-multiplier"));
//         });
//     });

//     function calculateScore() {
//         let inputNumber = parseFloat(document.getElementById("input-number").value);
//         if (!isNaN(inputNumber)) {
//             let newScore = inputNumber * selectedMultiplier;
//             document.getElementById("score").textContent = newScore.toFixed(2);
//         } else {
//             alert("Iltimos, son kiriting!");
//         }
//     }