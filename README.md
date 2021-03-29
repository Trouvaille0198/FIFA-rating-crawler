# FIFA-rating-crawler

## 目标内容
- 正数url
    https://www.futhead.com/21/players/?page={}&level=all_nif&bin_platform=pc
    1-209
- 倒数url
    https://www.futhead.com/21/players/?sort=-rating&level=all_nif&page={}&bin_platform=pc
    1-136
- 具体内容页
    https://www.futhead.com/21/players/20406/

## Xpath
- 球员详情页 url
    //div[@class='row']//div[@class='col-flex-300']/ul/li/div/a[@class='display-block padding-0']/@href
    
    或
    
    //a[@class='display-block padding-0']
    
- 球员资料
  - 头像地址 url
    //div[@class='row']//div[@class='playercard-picture']/img/@src
  - 球员能力
    - position
      //div[@class='row']//div[@class='playercard-position']/text()
      
    - rating
      //div[@class='row']//div[@class='playercard-rating']/text()
      
    - PACE
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr1']/span[@class='chembot-value']/text()
      
      - Acceleration
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Acceleration']/../span[contains(@class,'player-stat-value ')]
      
      - Sprint Speed
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Sprint Speed']/../span[contains(@class,'player-stat-value ')]
      
    - SHOOTING
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr2']/span[@class='chembot-value']/text()
      
      - Positioning
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Positioning']/../span[contains(@class,'player-stat-value ')]
      
      - Finishing
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Finishing']/../span[contains(@class,'player-stat-value ')]
      
      - Shot Power
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Shot Power']/../span[contains(@class,'player-stat-value ')]
      
      - Long Shots
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Long Shots']/../span[contains(@class,'player-stat-value ')]
      
      - Volleys
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Volleys']/../span[contains(@class,'player-stat-value ')]
      
      - Penalties
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Penalties']/../span[contains(@class,'player-stat-value ')]
      
    - PASSING
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr3']/span[@class='chembot-value']/text()
      
      - Vision
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Vision']/../span[contains(@class,'player-stat-value ')]
      
      - Crossing
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Crossing']/../span[contains(@class,'player-stat-value ')]
      
      - Free Kick
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Vision']/../span[contains(@class,'player-stat-value ')]
      
      - Short Passing
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Free Kick']/../span[contains(@class,'player-stat-value ')]
      
      - Long Passing
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Long Passing']/../span[contains(@class,'player-stat-value ')]
      
      - Curve 
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Curve']/../span[contains(@class,'player-stat-value ')]
      
    - DRIBBLING
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr4']/span[@class='chembot-value']/text()
      
      - Agility
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Agility']/../span[contains(@class,'player-stat-value ')]
      
      - Balance
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Balance']/../span[contains(@class,'player-stat-value ')]
      
      - Reactions
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Reactions']/../span[contains(@class,'player-stat-value ')]
      
      - Ball Control
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Ball Control']/../span[contains(@class,'player-stat-value ')]
      
      - Dribbling
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Dribbling']/../span[contains(@class,'player-stat-value ')]
      
      - Composure
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Composure']/../span[contains(@class,'player-stat-value ')]
      
    - DEFENSE
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr5']/span[@class='chembot-value']/text()
      
      - Interceptions
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Interceptions']/../span[contains(@class,'player-stat-value ')]
      
      - Heading
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Heading']/../span[contains(@class,'player-stat-value ')]
      
      - Def. Awareness
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Def. Awareness']/../span[contains(@class,'player-stat-value ')]
      
      - Standing Tackle
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Standing Tackle']/../span[contains(@class,'player-stat-value ')]
      
      - Sliding Tackle
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Sliding Tackle']/../span[contains(@class,'player-stat-value ')]
      
    - PHYSICAL
      
      //div[@class='row']//div[@class='playercard-attr playercard-attr6']/span[@class='chembot-value']/text()
      
      - Jumping
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Jumping']/../span[contains(@class,'player-stat-value ')]
      
      - Stamina
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Stamina']/../span[contains(@class,'player-stat-value ')]
      
      - Strength
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Strength']/../span[contains(@class,'player-stat-value ')]
      
      - Aggression
      
          //div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Aggression']/../span[contains(@class,'player-stat-value ')]
  - 球员资料
    - Full name
    
        //ul[@class='list-group margin-b-8']//div[@class='font-16 fh-red']/a/text()
    
    - Club
    
        //ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()
    
    - League
    
        //ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()
    
    - Nation
    
        //ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()
    
    - Age
    
        //div[@class='col-xs-7' and text()='Age']/../div[@class='col-xs-5 player-sidebar-value']/text()
    
        33 - 24/06/1987
    
    - Height
    
        //div[@class='col-xs-7' and text()='Height']/../div[@class='col-xs-5 player-sidebar-value']/text()
    
        170cm | 5'7"
    
        