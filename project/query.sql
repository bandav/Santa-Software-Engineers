SELECT * FROM gift;

SELECT * FROM liked_gift;

SELECT * FROM user;

SELECT * FROM liked_gift WHERE liked_id = current_user.username
SELECT * FROM liked_gift WHERE liking_id = 1;


DELETE FROM gift WHERE id=1;

DELETE FROM liked_gift where liking_id=1;

INSERT INTO gift VALUES(0, "YSL Tote", 1000, "Pretty", "", 0);
INSERT INTO gift VALUES(1, "Teddy Bear", 10, "So cute", "", 0);
