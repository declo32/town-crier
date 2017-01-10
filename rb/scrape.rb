require 'nokogiri'
require 'open-uri'
require 'json'
require 'twitter'
require 'time'
require 'mechanize'
require 'uri'
require 'fileutils'

$client=Twitter::REST::Client.new do |config|
    config.consumer_key        = "CONSUMER_KEY"
    config.consumer_secret     = "CONSUMER_SECRET"
    config.access_token        = "ACCESS_TOKEN"
    config.access_token_secret = "ACCESS_SECRET"
end

#turns the url into a Nokogiri object
def parse_url url
    html=[]
    begin
        open(url){|f|
            f.each_line{|l| html << l}
        }
    rescue RuntimeError
        puts "\tThe link provided: #{url} redirects to a different link, which is forbidden"
    end
    return Nokogiri::HTML(html * "")
end
#gets the first announcement of the archive list. The most recent link is at index 2. Indexes 0 and 1 are some aspen jumble.
#The most recent article is locked at the css selector "tr a"
#If SHS updates the way announcements are displayed in the archive, the css selectors will have to change.
def get_latest_announcement
    doc=parse_url "http://www.scituate.k12.ma.us/index.php/about-shs/daily-announcements-archive"
    return "http://www.scituate.k12.ma.us#{doc.css("tr a")[2]['href']}"
end

#This gets the article body's html. This will return the full announcement, images, styles and all.
#For now, the article body can be located via the css selector of "#hpBot #rightCol .item-page [itemprop='articleBody']". 
#This might change if SHS updates their website to use a different provider. Beware!
def get_announcement_info url
    doc=parse_url(url)
    return doc.css("#hpBot #rightCol .item-page [itemprop='articleBody']")
end

#Provided the type(school, tweet), the author(SHS, @SHSFacts, etc.) and the announcement(full html, tweet body, etc.) this method will return
#the hash version of that, which will eventually be turned into JSON format.
def export_announcement type, author, announcement
    return {:type=>type, :author=>author, :body=>announcement}
end
#Gets the list of users from the users.txt file.
def get_users
    users=[]
    open("users.txt"){|f|
        f.each_line{|l| users << l}
    }
    return users;
end

#This gets the tweet's user, message, and image(if it has one) into a hash.
#The picture is found at the css selector, "div.AdaptiveMedia .AdaptiveMedia-container .AdaptiveMedia-singlePhoto .AdaptiveMedia-photoContainer img"
#if twitter changes how these are displayed, then the css selectors will have to change.
#the image is downloaded into the "img" folder. The file path is included in the hash.
def get_tweets user, age
    tweets=[]
    begin
        $client.user_timeline(user).each{|t|
            tweet={}
            tweet[:user]=user
            tweet[:profile]="./profiles/#{user.strip}.jpg"
            if (t.created_at.yday-Time.now.yday).abs <=7
                tweet[:message]=t.text
                if(t.text.include? "https://t.co")
                    link=URI.extract(t.text, ["http", "https"])
                    tweet[:img]=get_picture link[0]
                end
                tweets << tweet
            end
        }
        return tweets
    rescue Twitter::Error::NotFound
        puts "\tERROR: User: \"#{user.strip}\" is not found"
        return []
    end
end

#downloads the picture into the "img" folder and returns the file path.
#The picture is found at the css selector "div.AdaptiveMedia .AdaptiveMedia-container .AdaptiveMedia-singlePhoto .AdaptiveMedia-photoContainer img"
def get_picture url
    doc=parse_url url
    selector="div.AdaptiveMedia .AdaptiveMedia-container .AdaptiveMedia-singlePhoto .AdaptiveMedia-photoContainer img"
    pic=doc.css("div.AdaptiveMedia .AdaptiveMedia-container .AdaptiveMedia-singlePhoto .AdaptiveMedia-photoContainer img");
    begin
        src=pic[0]['src']
        file_name="./img/#{src["https://pbs.twimg.com/media/".length...src.length]}"
        agent=Mechanize.new
        agent.get(src).save file_name
        return file_name
    rescue NoMethodError
        puts "\tError: The link is not a picture"
    end
end

#gets the profile pictures from all the users in the users.txt file.
def get_profile_pic user_list
    FileUtils.rm_rf("./profiles/")
    profile_urls=[]
    agent=Mechanize.new
    user_list.each do |u|
        begin
            pic=$client.user(u).profile_image_uri_https(size=:original)
            profile_urls << pic
            file_name="./profiles/"+u.strip+".jpg"
            agent.get(pic).save file_name
        rescue Twitter::Error::NotFound
            puts "#{u} was not found"
        end
    end
    return profile_urls
end
#puts the supplied tweet object into an html format. 
def create_tweet tweet
    return <<-EOT
    <img class="profile-pic" src="#{tweet[:profile]}"></img>
    <h1 class="user">#{tweet[:user]}</h1>
    <h3 class="message">#{tweet[:message]}</h3>
    <img class="tweet-image" src="#{tweet[:img]}"></img>
    <br>
    EOT
end

#creates the slide.html file for the front-end.
def create_slide
    #clears the img folder
    FileUtils.rm_rf("./img/")
    slide=[]
    puts "Getting school website information"
    slide << get_announcement_info(get_latest_announcement)
    users=get_users
    get_profile_pic users
   seconds_per_week=604800*1000

    users.each do |u|
        puts "Scraping tweets from #{u}"
        get_tweets(u, seconds_per_week).each do |t|
            slide << create_tweet(t)
        end
    end
    File.open("slide.html", "w") do |f|
        slide.each do |l|
            f.puts l
        end
    end
end

create_slide
