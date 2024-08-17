-- SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student
-- input: user_id
DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(5,2);

    -- Calculate the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Insert or update the average score in the average_scores table
    INSERT INTO average_scores (user_id, avg_score)
    VALUES (user_id, avg_score)
    ON DUPLICATE KEY UPDATE avg_score = avg_score;
    
END $$

DELIMITER ;
