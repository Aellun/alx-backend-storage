-- SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student
-- input: user_id
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    -- Update the users table with the computed average score
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE corrections.user_id = user_id
    )
    WHERE id = user_id;

END $$

DELIMITER ;
