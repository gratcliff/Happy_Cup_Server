happy_cup.factory('content_factory', function($http, $interval){

	var factory = {};
	var content = {};


	factory.getContent = function(callback){

			$http.get('content/').then(function(response){
				content.home = response.data.home;
				console.log(content.home.products);
				content.about = response.data.about;
				content.locations = response.data.locations;
				content.blog = response.data.blogPosts;
				content.stripe_public_key = response.data.stripe_public_key;
				content.global = {
				headerLogo : "https://dl.dropboxusercontent.com/u/8287719/resources/images/Banners/HC_Logo.png",
				};
		
				// content.blog = [
				// 	{
				// 		id: 1,
				// 		title: 'onlyinyourstate.com named Happy Cup one of the 12 unique shops to visit in Oregon',
				// 		description: 'Based in Portland, Happy Cup is a unique cafe and coffee roaster using ethicially traded coffee sourced from all over the world. The humanitarian, community oriented company offers employment to adults with disabilities and donates a percentage of their profits to vocational and recreational programming for the disabled community.',
				// 		link_title: 'Full Life Launches Sustainable Coffee Roasting Business',
				// 		url: 'http://www.onlyinyourstate.com/oregon/coffee-shops-oregon/',
				// 		img_url: staticURL+'website/resources/images/blog/2016/01/21/1.jpg',
				// 		text: '<p> Based in Portland, Happy Cup is a unique cafe and coffee roaster using ethicially traded coffee sourced from all over the world. The humanitarian, community oriented company offers employment to adults with disabilities and donates a percentage of their profits to vocational and recreational programming for the disabled community. Plus, their coffee is delicious! My personal favorite is the Boom Boom dark roast. Read the full article <a href="http://www.onlyinyourstate.com/oregon/coffee-shops-oregon/">here.</a></p>',
				// 		created_at: '2016-01-21T16:15:37+00:00',
				// 		updated_at: '2016-01-21T16:15:37+00:00',
				// 	},
				// 	{
				// 		id: 2,
				// 		title: 'Happy Cup Killingsworth named one of Portland’s top 10 new cafes',
				// 		description: 'Read Willamette Week’s write up featuring Happy Cup Killingsworth as one of the ten best new cafes in Portland for 2015.',
				// 		link_title: 'Full article here!',
				// 		url: 'http://www.wweek.com/2015/11/10/the-10-best-new-coffee-shops-in-portland/',
				// 		img_url: staticURL+'website/resources/images/blog/2015/11/11/1.jpg',
				// 		text: '<p> Read Willamette Week’s write up featuring Happy Cup Killingsworth as one of the ten best new cafes in Portland for 2015.</p> <p>Happy Cup Coffee</p><br><p>446 NE Killingsworth St., 889-0511, <a href = "www.happycup.com">happycup.com</a> <p>Happy Cup exists sort of as an ode to squishy feelings: When I walked into a backroom stacked with beanbags at Happy’s newest location on Killingsworth Street, Portland entertainer Nikki Brown Clown was in the back setting up a book table for her Tuesday-morning gig entertaining preschoolers. Other days, the room might house a sewing club, a book group, or a small press reading. Meanwhile, the coffee is roasted in part by adults with disabilities, and the proceeds from the three cafes flip out to related programs. It’s hard not to feel good about it all. But this is the thing: It’s also one of the better examples of a solidly domestic cafe in town, with decent coffee, two neat copies of&nbsp;<i>The New York Times</i>&nbsp;laid out each day in a gesture of squarely old-school hospitality, an array of couches neither too soft nor too hard, and plenty of corners where you can plug in a laptop or just plain hide. A word, however: That piano in the back looks nice, but don’t sit by it. Just…trust me on that. MATTHEW KORFHAGE.</p> <a href = "http://www.wweek.com/2015/11/10/the-10-best-new-coffee-shops-in-portland/">Full article here!</a>',
				// 		created_at: '2015-11-11T14:04:56+00:00',
				// 		updated_at: '2015-11-11T14:04:56+00:00',
				// 	},
				// 	{
				// 		id: 3,
				// 		title: 'Jobs & Hope', 
				// 		description: 'The Portland Observer stopped by Happy Cup on Killingsworth and came away with an article focused on our mission and the different ways Happy Cup is working to benefit adults with developmental disabilities.',
				// 		link_title: 'Read the full article here',
				// 		url: 'http://portlandobserver.com/news/2015/mar/03/jobs-and-hope/',
				// 		img_url: staticURL+'website/resources/images/blog/2015/03/6/1.jpg',
				// 		text: '<p> The Portland Observer stopped by Happy Cup on Killingsworth and came away with an article focused on our mission and the different ways Happy Cup is working to benefit adults with developmental disabilities.  “A small corner of northeast Portland is expanding to create more jobs and hope for adults with developmental disabilities.” </p> <a href = "http://portlandobserver.com/news/2015/mar/03/jobs-and-hope/">Read the full article here</a>.',
				// 		created_at: '2015-03-06T15:24:05+00:00',
				// 		updated_at: '2015-03-06T15:24:05+00:00',
				// 	}, 
				// 	{
				// 		id: 4, 
				// 		description: 'Happy Cup continues to expand opening a third location at 446 NE Killingsworth.  The location serves as the flagship locale for Happy Cup and offers unique single origin coffees as well as a full breakfast and lunch menu.',
				// 		title: 'New Cafe opening on Killingsworth & MLK',
				// 		link_title: ['here', 'here'],
				// 		url: ['http://www.bizjournals.com/portland/blog/sbo/2014/11/socially-minded-happy-cup-coffee-co-adding-a-third.html', 'http://www.bizjournals.com/portland/blog/sbo/2015/01/happy-cup-with-opening-of-new-portland-caf-the.html?ana=twt'],
				// 		img_url: staticURL+'website/resources/images/blog/2015/01/15/2.jpg',
				// 		text: '<p> Happy Cup continues to expand opening a third location at 446 NE Killingsworth.  The location serves as the flagship locale for Happy Cup and offers unique single origin coffees as well as a full breakfast and lunch menu.  Come have a pour over and experience the Happy Cup mission.  For more information check the cafe section of our website and read the articles <a href = "http://www.bizjournals.com/portland/blog/sbo/2014/11/socially-minded-happy-cup-coffee-co-adding-a-third.html">here</a> and <a href = "http://www.bizjournals.com/portland/blog/sbo/2015/01/happy-cup-with-opening-of-new-portland-caf-the.html?ana=twt">here</a>.</p>',
				// 		created_at: '2015-01-15T21:13:19+00:00',
				// 		updated_at: '2015-01-15T21:13:19+00:00',
				// 	}, 
				// 	{
				// 		id: 5,
				// 		description: 'Happy Cup was honored by the Portland Business Journal for creating sustainable jobs for the Portland community.  Read about the awards here.  We are grateful for the award and want to send a huge thank you to all of Portland for your support!',
				// 		title: 'Happy Cup Wins Innovation in Sustainability Award 2014',
				// 		url: 'http://www.bizjournals.com/portland/blog/sbo/2014/11/meet-the-innovation-in-sustainability-winners.html',
				// 		img_url: staticURL+'website/resources/images/blog/2015/01/15/1.jpg',
				// 		text: '<p>Happy Cup was honored by the Portland Business Journal for creating sustainable jobs for the Portland community. &nbsp;Read about the awards <a href="http://www.bizjournals.com/portland/blog/sbo/2014/11/meet-the-innovation-in-sustainability-winners.html">here</a>. &nbsp;We are grateful for the award and want to send a huge thank you to all of Portland for your support!</p>',
				// 		created_at: '2015-01-15T21:03:11+00:00',
				// 		updated_at: '2015-01-15T21:03:11+00:00',
				// 	}, 
				// 	{
				// 		id: 6, 
				// 		description: 'At Happy Cup Coffee Company in City Hall one afternoon, barista Caitlin Lawson coached Keyona, 28, through the register, checking out an iced coffee order.',
				// 		title: 'Happy Cup Embodies Portland\'s Progressive Values',
				// 		img_url: staticURL+'website/resources/images/blog/2014/08/19/1.jpg', 
				// 		other_img_url: staticURL+'website/resources/images/blog/2014/08/19/2.jpg',
				// 		text: '<div class="entry_content"><p>Mayor Hales Supports Shriver Report’s ‘City-Festo’ for Women’s, Other Groups’ Empowerment</p><p>FRIDAY, JULY 18, 2014 — At&nbsp;<a href="http://happycup.com/">Happy Cup Coffee Company</a>&nbsp;in City Hall one afternoon, barista Caitlin Lawson coached Keyona, 28, through the register, checking out an iced coffee order.</p><p></p><p>Happy Cup — with its coffee roasting operation and two café locations — is a program through&nbsp;<a href="http://www.fulllife.com/">Full Life</a>, an organization that employs developmentally disabled adults like Keyona who want to work for minimum wage or better with benefits, job counseling, and other services. Full Life was founded 12 years ago by a woman who championed opportunities for disabled adults.</p><p>“It’s fun,” says Keyona, who has worked with Full Life for seven years. “I get to work with different people. It gives me a different outlook and perspective on life.”</p><p>The city has supported Happy Cup’s mission, helping it into the City Hall location and into a Northeast Portland space near the Portland Police Bureau’s North Precinct.</p><p>Such support is why<a href="http://mariashriver.com/">&nbsp;Maria Shriver</a>, founder of&nbsp;<a href="http://shriverreport.org/">Shriver Report</a>, praised Mayor Charlie Hales at the<a href="https://www.facebook.com/PDXMayor.charlie.hales/media_set?set=a.299961633514337.1073741829.100005015072832&amp;type=3">&nbsp;U.S. Conference of Mayors</a>&nbsp;in June for Portland’s progressive and innovative efforts to create an equitable city. Shriver Report is a nonprofit online platform through which women and others may share stories of progress in overcoming inequity. At the U.S. Conference of Mayors, Shriver’s organization distributed a<a href="http://shriverreport.org/the-city-festo-10-ways-to-move-your-city-forward/">“city-festo,” a guide to implementing policies that support families and work to empower both women and men to be successful in their cities</a>.</p><p>In addition to existing policies and advocacy at the city, state and federal level, Hales is supporting Shriver Report’s call for city leaders to be “architects of change,” encouraging policies that support women and families through education, involvement and outreach.</p><p>“Happy Cup embodies Portland’s progressive values,” says Hales, who visits the City Hall café for coffee and salads. “We’re a city that cares for its people, and we put our progressive values into practice.”</p><p>The mayor has thrown his support behind the “city-festo” as another step in overcoming historical inequities to make the city more livable for everyone.</p><p>“Portland is a deliberately family-friendly city,” Hales says. “We’re continuing to work to make sure every resident lives in a complete neighborhood, with parks full of amenities, streets and sidewalks in good repair, and equal opportunities for successful futures.”</p><p>The “city-festo” calls for an informed community, 100 percent voter registration, and education, encouraging city officials to teach equity through leadership, policies and practices.</p><p>Hales, through diversity workshops such as&nbsp;<a href="http://www.portlandoregon.gov/mayor/article/438858">White Men as Full Diversity Partners</a>&nbsp;and outreach initiatives such as&nbsp;<a href="http://instagram.com/p/qXfAb5semC/?modal=true">Black Male Achievement</a>, has led Portland through many of the report’s 10 steps to build change.</p><p>Likewise, the city has made progress through Commissioner Amanda Fritz’s citywide paid sick leave policy; sick leave was the No. 1 policy that women who were surveyed said they needed from their city. Shriver told Hales that Portland’s policy is an exemplar for cities nationwide.</p><p>Through Black Male Achievement, Hales led community leaders in collaboratively developing programs to support young, African-American men, who disproportionately experience high incarceration, dropout and unemployment rates. SummerWorks, whose second-largest funder is the city, finds summer internships for at-risk teenagers, helping them stay on the right track. City Hall this year hired 100 interns.</p><p>Hales, through the U.S. Conference of Mayors, has advocated for comprehensive immigration reform at the federal level. At the state level, the city has advocated for statewide sick leave, affordable housing non-discrimination legislation, tuition equity, and for funding pilot programs to build of Portland Community College’s successful Future Connect scholarship program, which seeks to eliminate financial barriers to college. Last year the City Council passed two affordable housing policies that were key to preserving affordable housing units in Portland. One continued a tax abatement program to create an incentive for developers to build affordable housing, and another clarified that affordable housing on city property is tax-exempt.</p><p><img class="alignleft" title="Caitlin Lawson makes a latte with Keyona at Happy Cup in City Hall." alt="Caitlin Lawson and Keyona at Happy Cup" src="http://www.portlandoregon.gov/shared/cfm/image.cfm?id=497260" width="250" height="174">And the city supports businesses like Happy Cup.</p><p>“Happy Cup establishes challenges that not every service job gives you,” says Lawson, the barista. “The relationships we build with Full Life clients make the job so much more fulfilling.”</p><p>ShriverReport’s “city-festo” gives the city more equity goals to pursue — 100 percent voter registration, addressing inequities across the city, empowering oftentimes marginalized populations.</p><p>“The ‘city-festo’ is a great list of goals that Portland is capable of achieving,” Hales says. “We’ve made tremendous progress over the last year-and-a-half. Now it’s time to focus our energies on making this city truly equitable for all genders, all races, all sexual orientations — all citizens.”</p></div>',
				// 		created_at: '2014-08-19T10:02:09+00:00',
				// 		updated_at: '2014-08-19T10:02:09+00:00',
				// 	}, 
				// 	{
				// 		id: 7,
				// 		description: 'Happy Cup Opens Flagship Cafe In Portland City Hall',
				// 		title: 'Happy Cup Opens Flagship Cafe In Portland City Hall',
				// 		url: 'http://sprudge.com/happy-cup-coffee-and-food-carts-at-portland-city-hall-portland-52047.html',
				// 		img_url: staticURL+'website/resources/images/blog/2014/03/20/1.jpg', 
				// 		text: '<p>Thanks to Hannah Neuschwander and Sprudge.com for the post featuring our City Hall Cafe. &nbsp;We are excited to be in City Hall, and as Mayor Hales says ““Happy Cup represents a great opportunity for us to draw people into City Hall. We don’t want to be a place that people go only when there is a problem—we want to be an inviting and integrated part of the community.”</p><a href="http://sprudge.com/happy-cup-coffee-and-food-carts-at-portland-city-hall-portland-52047.html" >Check it out!</a>',
				// 		created_at: '2014-03-20T13:23:27+00:00',
				// 		updated_at: '2014-03-20T13:23:27+00:00',
				// 	}, 
				// 	{
				// 		id: 8,
				// 		description: 'In an ongoing effort by Mayor Charlie Hales to encourage more Portlanders to visit City Hall, Happy Cup Coffee Co. is building out a flagship cafe to serve city staffers and visitors.',
				// 		title: 'Social enterprise coffee shop to open in Portland City Hall',
				// 		url: 'http://www.bizjournals.com/portland/blog/sbo/2014/01/social-enterprise-coffee-shop-to-open.html',
				// 		img_url: staticURL+'website/resources/images/blog/2014/03/20/2.jpg',
				// 		text: '<p>Portland City Hall has invited a mission-focused coffee roaster to set up shop in downtown Portland.</p><p class="content__segment">In an ongoing effort by Mayor <a href="portland/search/results?q=Charlie Hales">Charlie Hales</a> to encourage more Portlanders to visit City Hall, <a href="http://happycup.com/" target="_blank">Happy Cup Coffee Co.</a> is building out a flagship cafe to serve city staffers and visitors.</p><p class="content__segment">Happy Cup, a social enterprise run by <a href="http://www.fulllife.com/" target="_blank">Full Life</a>, was <a href="http://www.sustainablebusinessoregon.com/articles/2011/12/full-life-launches-sustainable-coffee.html" target="_blank">established in 2011</a> to provide employment and recreational opportunities for people with disabilities.</p><p class="content__segment">"This is our chance to really showcase our mission and our coffee in a great location," said <a href="portland/search/results?q=Adam Bray">Adam Bray</a>, Happy Cup\'s operations director.</p>',
				// 		created_at: '2014-03-20T13:00:31+00:00',
				// 		updated_at: '2014-03-20T13:00:31+00:00',
				// 	},
				// 	{
				// 		id: 9,
				// 		description: 'Spectrums Magazine is Portland and SW Washington’s only magazine devoted to Autism Spectrum Disorder, and they did a great feature on Bill Snell a member of our production crew.  Take a look to see pictures of the crew in action and read about all the things Bill does at Happy Cup.',
				// 		title: 'Spectrums Magazine feature on Happy Cup production crew',
				// 		url: 'https://issuu.com/courtneyfreitag/docs/spectrums_magazine_fall13_web?e=0/4769599',
				// 		img_url: staticURL+'website/resources/images/blog/2013/09/10/1.jpg',
				// 		text: '<p>Spectrums Magazine is Portland and SW Washington’s only magazine devoted to Autism Spectrum Disorder, and they did a great feature on Bill Snell a member of our production crew. &nbsp;Take a look to see pictures of the crew in action and read about all the things Bill does at Happy Cup.</p><p><a href="http://issuu.com/courtneyfreitag/docs/spectrums_magazine_fall13_web?e=0/4769599"><img class="alignnone size-medium wp-image-724" alt="Spectrums cover" src="http://happycup.com/wp-content/uploads/2013/09/Spectrums-cover-235x300.jpg" width="235" height="300"></a></p>',
				// 		created_at: '2013-09-10T10:53:55+00:00',
				// 		updated_at: '2013-09-10T10:53:55+00:00',
				// 	}, 

				// ];

			content.contact = {

			};
		

			content.cafe = {

			};

				callback(content);

			});

		
	}

	factory.getPageContent = function(page, callback) {

		var waitForContent = $interval(function(){
			if (content[page] !== undefined) {
				$interval.cancel(waitForContent);
				callback(content[page]);
			} 

		},10)

	}


	return factory;
});