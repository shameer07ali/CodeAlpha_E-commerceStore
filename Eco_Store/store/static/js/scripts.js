document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.animated-content');

    const checkVisibility = () => {
        animatedElements.forEach(element => {
            const rect = element.getBoundingClientRect();

            // Check if the element is within the viewport
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                // Add animation classes based on the element's assigned animation
                if (element.classList.contains('bounce-in')) {
                    element.classList.add('bounce-in');
                }
                if (element.classList.contains('fade-in')) {
                    element.classList.add('fade-in');
                }
                if (element.classList.contains('slide-in')) {
                    element.classList.add('slide-in');
                }
                if (element.classList.contains('fade-out')) {
                    element.classList.remove('fade-in'); // Remove any fade-in if exists
                    element.classList.add('fade-out');
                }
            }
        });
    };

    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // Check visibility on page load
});
//for home page to show products 
document.addEventListener('DOMContentLoaded', function() {
    const productScroller = document.querySelector('.product-scroller');

    productScroller.addEventListener('wheel', (evt) => {
        evt.preventDefault();
        productScroller.scrollLeft += evt.deltaY;
    });
});
