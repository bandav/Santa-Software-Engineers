SELECT * FROM gift;

SELECT * FROM liked_gift;
SELECT * FROM joined_game;

SELECT * FROM user;

SELECT * FROM liked_gift WHERE liked_id = current_user.username
SELECT * FROM liked_gift WHERE liking_id = 1;


DELETE FROM gift WHERE id=0;
DELETE FROM gift WHERE id=1;
select * from game;

DELETE FROM liked_gift;

INSERT INTO gift VALUES(0, "YSL Tote", 1000, "Pretty", "", 0);
INSERT INTO gift VALUES(1, "Teddy Bear", 10, "So cute", "", 0);
INSERT INTO gift VALUES(0, "YSL Tote", 1000, "Pretty", "https://www.nordstrom.com/s/micro-toy-croc-embossed-patent-leather-shopper/6989910?color=1000+NERO&country=US&currency=USD&utm_source=google&utm_medium=organic&utm_campaign=seo_shopping&utm_channel=low_nd_seo_shopping", 0);
INSERT INTO gift VALUES(1, "Teddy Bear", 10, "So cute", "https://www.amazon.com/GUND-Ginger-Teddy-Stuffed-Animal/dp/B01NBKTSZ7/ref=asc_df_B01NBKTSZ7/?tag=hyprod-20&linkCode=df0&hvadid=312118126503&hvpos=&hvnetw=g&hvrand=16521001533200412149&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9016722&hvtargid=pla-525309281401&psc=1", 0);
INSERT INTO gift VALUES(3, "Six of Crows", 7, "Gripping novel about a heist!", "https://www.amazon.com/Six-of-Crows-Leigh-Bardugo-audiobook/dp/B012BNM1LO/ref=sr_1_1?crid=2JDKQGSJM84Y9&keywords=six+of+crows&qid=1670535367&sprefix=six+of+crow%2Caps%2C134&sr=8-1", 0);

