-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

-- Requirements:
    -- Procedure ComputeAverageScoreForUser is taking 1 input:
    -- user_id, a users.id value 
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser$$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    -- Update the user's average weighted score
    UPDATE users
    SET average_score = IFNULL((
        SELECT 
            SUM(corrections.score * projects.weight) / NULLIF(SUM(projects.weight), 0)
        FROM 
            corrections
        INNER JOIN 
            projects ON projects.id = corrections.project_id
        WHERE 
            corrections.user_id = user_id
    ), 0)
    WHERE id = user_id;
END $$

DELIMITER ;
