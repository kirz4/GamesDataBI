SELECT * FROM games_db.games;SELECT `games`.`id`,
    `games`.`name`,
    `games`.`platform`,
    `games`.`year`,
    `games`.`genre`,
    `games`.`publisher`,
    `games`.`na_sales`,
    `games`.`eu_sales`,
    `games`.`other_sales`,
    `games`.`global_sales`
FROM `games_db`.`games`;
