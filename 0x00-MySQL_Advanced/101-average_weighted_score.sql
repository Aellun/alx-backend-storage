-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

-- Requirements:

    -- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers$$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update the average weighted score for all users
    UPDATE users
    SET average_score = IFNULL((
        SELECT 
            SUM(corrections.score * projects.weight) / NULLIF(SUM(projects.weight), 0)
        FROM 
            corrections
        INNER JOIN 
            projects ON projects.id = corrections.project_id
        WHERE 
            corrections.user_id = users.id
    ), 0);
END $$

DELIMITER ;
