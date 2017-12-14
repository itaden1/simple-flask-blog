window.onload = function(){
	//var text = getText();
	//changeImage.init();
	var responsiveNav = new navResponsive();
	responsiveNav.init('nav-collapse','icon');

	var scroll_top = new pageScroll();
	scroll_top.init('top','body-top',600, 15);
	var scroll_projects = new pageScroll();
	scroll_projects.init('projectsBtn','projects',600, 15);
	var scroll_skills = new pageScroll();
	scroll_skills.init('skillsBtn','skills',600, 15);
	var scroll_about = new pageScroll();
	scroll_about.init('aboutBtn','about',600, 15);

	var myCarousel = new carousel()
	myCarousel.init('carousel',6000)
	var subHeadCarousel = new carousel()
	subHeadCarousel.init('subhead',6000)

}
