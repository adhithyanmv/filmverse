const pageleft = document.querySelector(".pageleft");
const pageright = document.querySelector(".pageright");
const pagecurr = document.querySelector(".pagecurr");
const videoTrailer = document.querySelector(".videoTrailer");
const overlay = document.querySelector(".overlay");
const upcoming = document.querySelector(".uc");
const popular = document.querySelector(".popular");
const topRated = document.querySelector(".tr");
const navLinks = document.querySelectorAll(".nav-link");
const bannermoviename = document.querySelector(".bannermoviename");
const bannermoviedesc = document.querySelector(".bannermoviedesc");
const bannerimage = document.getElementById("hero");
const mvimg = document.querySelectorAll(".mvimg");
const trailers = document.querySelectorAll(".videoTrailer");
const iconBox = document.querySelectorAll(".icon-box");
const toggleBtn = document.querySelector("#toggle");

function check() {
  let theme = window.localStorage.getItem("theme");
  if (theme === "dark") {
    toggleBtn.classList.add("active");
    makeDark();
  }
}

check();

popular.addEventListener("click", (e) => {
  if (popular.classList.contains("active")) {
    return;
  }
  popular.classList.add("active");
  upcoming.classList.remove("active");
  topRated.classList.remove("active");
  setMovies();
});

function makeDark() {
  window.localStorage.setItem("theme", "dark");
  document.querySelectorAll(".icon-box").forEach((e) => {
    e.style.backgroundColor = "rgb(56, 54, 54)";
  });
  document.querySelector("#icon-boxes").style.backgroundColor = "black";
  document.querySelector(".pagination").style.backgroundColor = "black";
  document.querySelectorAll(".page-link").forEach((e) => {
    e.style.backgroundColor = "black";
  });
  document.querySelector("body").style.backgroundColor = "black";
}

function makeDefault() {
  window.localStorage.setItem("theme", "default");
  document.querySelectorAll(".icon-box").forEach((e) => {
    e.style.backgroundColor = "white";
  });
  document.querySelector("#icon-boxes").style.backgroundColor = "white";
  document.querySelector(".pagination").style.backgroundColor = "white";
  document.querySelectorAll(".page-link").forEach((e) => {
    e.style.backgroundColor = "white";
  });
  document.querySelector("body").style.backgroundColor = "white";
}

function toggle(x) {
  x.classList.toggle("active");
  if (x.classList.contains("active")) {
    makeDark();
  } else {
    makeDefault();
  }
}

upcoming.addEventListener("click", (e) => {
  if (upcoming.classList.contains("active")) {
    return;
  }
  upcoming.classList.add("active");
  popular.classList.remove("active");
  topRated.classList.remove("active");
  setMovies();
});

topRated.addEventListener("click", (e) => {
  if (topRated.classList.contains("active")) {
    return;
  }
  topRated.classList.add("active");
  upcoming.classList.remove("active");
  popular.classList.remove("active");
  setMovies();
});

function category() {
  let data = "Popular";

  for (let i = 0; i < navLinks.length; i++) {
    if (navLinks[i].classList.contains("active")) {
      data = navLinks[i].textContent;
      break;
    }
  }
  return data;
}

function setMovies(pageNo = 1) {
  overlay.style.visibility = "visible";
  let datas = movieDealer(category(), pageNo);
  let movieNames = document.querySelectorAll(".moviename");
  let movieImgs = document.querySelectorAll(".mvimg");
  let stars = document.querySelectorAll(".rate");
  let movienamelink = document.querySelectorAll(".movienamelink");
  let starsArr = convertStars(stars);
  emptyStars(stars);
  datas.then((e) => {
    let result = e.results;
    for (let i = 0; i < result.length; i++) {
      let curr = result[i];
      movieNames[i].textContent = curr.original_title
        ? curr.original_title
        : curr.original_name;
      movieImgs[i].src = `https://image.tmdb.org/t/p/original${
        curr.poster_path ? curr.poster_path : curr.backdrop_path
      }`;
      if (curr.media_type == "movie") {
        movienamelink[i].setAttribute("href", `movie/${curr.id}/`);
      }
      if (curr.media_type == "tv") {
        movienamelink[i].setAttribute("href", `tv/${curr.id}/`);
      }
      let currStars = starsArr[i];
      let totalRate = 0;
      if (Math.floor(curr.vote_average - 1) % 2 == 1) {
        totalRate += Math.floor((curr.vote_average - 1) / 2);
        totalRate += 0.5;
      } else {
        totalRate += Math.floor(curr.vote_average / 2);
      }

      if (curr.vote_average && String(curr.vote_average).length > 2) {
        if (Number(String(curr.vote_average).slice(2)) > 0.5) {
          totalRate += 0.5;
        }
      }

      for (let j = 0; j < currStars.length; j++) {
        if (totalRate > 0.5) {
          currStars[j].classList.remove("bi-star");
          currStars[j].classList.add("bi-star-fill");
          totalRate -= 1;
        }
        if (totalRate === 0.5) {
          currStars[j].classList.remove("bi-star");
          currStars[j].classList.add("bi-star-half");
          totalRate = 0;
        }
      }
    }
  });
  overlay.style.visibility = "hidden";
}

function emptyStars(stars) {
  for (let i = 0; i < stars.length; i++) {
    if (stars[i].classList.contains("bi-star-half")) {
      stars[i].classList.remove("bi-star-half");
      stars[i].classList.add("bi-star");
    }
    if (stars[i].classList.contains("bi-star-fill")) {
      stars[i].classList.remove("bi-star-fill");
      stars[i].classList.add("bi-star");
    }
  }
}

function convertStars(stars) {
  let subArrays = [];
  let arr = [];
  for (let i = 0; i < stars.length; i++) {
    arr.push(stars[i]);
    if (arr.length === 5) {
      subArrays.push(arr);
      arr = [];
    }
  }
  return subArrays;
}

let SEARCHINGS = {
  trending:
    "https://api.themoviedb.org/3/trending/all/day?api_key=7afd10215ac669bb5736cf2a670d681e",
  theatre:
    "https://api.themoviedb.org/3/discover/movie?primary_release_date.gte=2022-07-10&primary_release_date.lte=2022-07-10&api_key=7afd10215ac669bb5736cf2a670d681e",
};

async function movieDealer(cg, pageno = 1) {
  if (cg == "Popular") {
    let res = await fetch(
      `https://api.themoviedb.org/3/trending/all/day?api_key=7afd10215ac669bb5736cf2a670d681e&page=${pageno}`
    );
    let data = await res.json();
    return data;
  }

  if (cg == "Top Rated") {
    let res = await fetch(
      `https://api.themoviedb.org/3/movie/top_rated?api_key=7afd10215ac669bb5736cf2a670d681e&page=${pageno}`
    );
    let data = await res.json();
    return data;
  }

  if (cg == "Upcoming") {
    let res = await fetch(
      `https://api.themoviedb.org/3/movie/upcoming?api_key=7afd10215ac669bb5736cf2a670d681e&page=${pageno}`
    );
    let data = await res.json();
    return data;
  }
}

if (location.hash.slice(1)) {
  setMovies(location.hash.slice(1));
} else {
  setMovies();
}

function bannerSet() {
  const trendings = movieDealer("Popular");
  trendings.then((e) => {
    const bannerLink = document.querySelector(".bannerLink");
    const bannerData = e.results[Math.floor(Math.random() * 20)];
    bannermoviename.textContent = bannerData.title
      ? bannerData.title
      : bannerData.original_title
      ? bannerData.original_title
      : bannerData.original_name;
    bannermoviedesc.textContent = bannerData.overview
      ? bannerData.overview
      : "";
    if (bannerData.media_type == "movie") {
      bannerLink.setAttribute("href", `movie/${bannerData.id}`);
    } else if (bannerData.media_type == "tv") {
      bannerLink.setAttribute("href", `tv/${bannerData.id}`);
    }

    bannerimage.style.backgroundImage = `url('https://image.tmdb.org/t/p/original${
      bannerData.backdrop_path
        ? bannerData.backdrop_path
        : bannerData.poster_path
    }')`;
    bannerimage.style.backgroundSize = "cover";
    bannerimage.style.backgroundRepeat = "no-repeat";
    bannerimage.style.backgroundSize = "cover";
    bannerimage.style.backgroundPosition = "center center";
  });
}
bannerSet();

window.addEventListener("hashchange", (e) => {
  setMovies(Number(location.hash.slice(1)));
  if (location.hash.slice(1) === 2 || !location.hash) {
    pageleft.classList.add("disabled");
  } else {
    pageleft.classList.remove("disabled");
  }
});

pageright.addEventListener("click", (e) => {
  let hash = Number(String(location.hash).slice(1));
  if (!hash) hash = 1;
  if (location.hash.slice(1) === 2 || !location.hash) {
    pageleft.classList.add("disabled");
  } else {
    pageleft.classList.remove("disabled");
  }
  pageright.setAttribute("href", `#${(hash += 1)}`);
  pagecurr.textContent = Number(pagecurr.textContent) + 1;
});

pageleft.addEventListener("click", (e) => {
  let hash = Number(String(location.hash).slice(1));
  if (!hash || hash === 2) {
    pageleft.classList.add("disabled");
    return;
  } else {
    pageleft.classList.remove("disabled");
  }
  pageleft.setAttribute("href", `#${(hash -= 1)}`);
  pagecurr.textContent = Number(pagecurr.textContent) - 1;
});

(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim();
    try {
      if (all) {
        return [...document.querySelectorAll(el)];
      } else {
        return document.querySelector(el);
      }
    } catch (e) {
      console.log(e);
    }
  };

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all);
    if (selectEl) {
      if (all) {
        selectEl.forEach((e) => e.addEventListener(type, listener));
      } else {
        selectEl.addEventListener(type, listener);
      }
    }
  };

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener("scroll", listener);
  };

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select("#navbar .scrollto", true);
  const navbarlinksActive = () => {
    let position = window.scrollY + 200;
    navbarlinks.forEach((navbarlink) => {
      if (!navbarlink.hash) return;
      let section = select(navbarlink.hash);
      if (!section) return;
      if (
        position >= section.offsetTop &&
        position <= section.offsetTop + section.offsetHeight
      ) {
        navbarlink.classList.add("active");
      } else {
        navbarlink.classList.remove("active");
      }
    });
  };
  window.addEventListener("load", navbarlinksActive);
  onscroll(document, navbarlinksActive);

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select("#header");
    let offset = header.offsetHeight;

    if (!header.classList.contains("fixed-top")) {
      offset += 70;
    }

    let elementPos = select(el).offsetTop;
    window.scrollTo({
      top: elementPos - offset,
      behavior: "smooth",
    });
  };

  /**
   * Header fixed top on scroll
   */
  let selectHeader = select("#header");
  let selectTopbar = select("#topbar");
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add("header-scrolled");
        if (selectTopbar) {
          selectTopbar.classList.add("topbar-scrolled");
        }
      } else {
        selectHeader.classList.remove("header-scrolled");
        if (selectTopbar) {
          selectTopbar.classList.remove("topbar-scrolled");
        }
      }
    };
    window.addEventListener("load", headerScrolled);
    onscroll(document, headerScrolled);
  }

  /**
   * Back to top button
   */
  let backtotop = select(".back-to-top");
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add("active");
      } else {
        backtotop.classList.remove("active");
      }
    };
    window.addEventListener("load", toggleBacktotop);
    onscroll(document, toggleBacktotop);
  }

  /**
   * Mobile nav toggle
   */
  on("click", ".mobile-nav-toggle", function (e) {
    select("#navbar").classList.toggle("navbar-mobile");
    this.classList.toggle("bi-list");
    this.classList.toggle("bi-x");
  });

  /**
   * Mobile nav dropdowns activate
   */
  on(
    "click",
    ".navbar .dropdown > a",
    function (e) {
      if (select("#navbar").classList.contains("navbar-mobile")) {
        e.preventDefault();
        this.nextElementSibling.classList.toggle("dropdown-active");
      }
    },
    true
  );

  /**
   * Scrool with ofset on links with a class name .scrollto
   */

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener("load", () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash);
      }
    }
  });

  /**
   * Preloader
   */
  // let preloader = select("#preloader");
  // if (preloader) {
  //   window.addEventListener("load", () => {
  //     preloader.remove();
  //   });
  // }

  /**
   * Clients Slider
   */
  new Swiper(".clients-slider", {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40,
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60,
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80,
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120,
      },
    },
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener("load", () => {
    let portfolioContainer = select(".portfolio-container");
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: ".portfolio-item",
        layoutMode: "fitRows",
      });

      let portfolioFilters = select("#portfolio-flters li", true);

      on(
        "click",
        "#portfolio-flters li",
        function (e) {
          e.preventDefault();
          portfolioFilters.forEach(function (el) {
            el.classList.remove("filter-active");
          });
          this.classList.add("filter-active");

          portfolioIsotope.arrange({
            filter: this.getAttribute("data-filter"),
          });
          portfolioIsotope.on("arrangeComplete", function () {
            AOS.refresh();
          });
        },
        true
      );
    }
  });

  /**
   * Initiate portfolio lightbox
   */
  const portfolioLightbox = GLightbox({
    selector: ".portfolio-lightbox",
  });

  /**
   * Initiate glightbox
   */
  const gLightbox = GLightbox({
    selector: ".glightbox",
  });

  /**
   * Portfolio details slider
   */
  new Swiper(".portfolio-details-slider", {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
  });

  /**
   * Animation on scroll
   */
  window.addEventListener("load", () => {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  });
})();
