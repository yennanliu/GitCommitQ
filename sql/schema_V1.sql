DROP SCHEMA IF EXISTS `gitcommit`;
CREATE SCHEMA IF NOT EXISTS `gitcommit` DEFAULT CHARACTER SET utf8 ;
USE `gitcommit`;

-- -----------------------------------------------------
-- Table `gitcommit`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`users` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `login` VARCHAR(255) NOT NULL COMMENT '',
  `company` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `type` VARCHAR(255) NOT NULL DEFAULT 'USR' COMMENT '',
  `fake` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '',
  `deleted` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '',
  `long` DECIMAL(11,8) COMMENT '',
  `lat` DECIMAL(10,8) COMMENT '',
  `country_code` CHAR(3) COMMENT '',
  `state` VARCHAR(255) COMMENT '',
  `city` VARCHAR(255) COMMENT '',
  `location` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`commits`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`commits` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`commits` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `sha` VARCHAR(40) NULL DEFAULT NULL COMMENT '',
  `author_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `committer_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `project_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  CONSTRAINT `commits_ibfk_1`
    FOREIGN KEY (`author_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `commits_ibfk_2`
    FOREIGN KEY (`committer_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `commits_ibfk_3`
    FOREIGN KEY (`project_id`)
    REFERENCES `gitcommit`.`projects` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`commit_parents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`commit_parents` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`commit_parents` (
  `commit_id` INT(11) NOT NULL COMMENT '',
  `parent_id` INT(11) NOT NULL COMMENT '',
  CONSTRAINT `commit_parents_ibfk_1`
    FOREIGN KEY (`commit_id`)
    REFERENCES `gitcommit`.`commits` (`id`),
  CONSTRAINT `commit_parents_ibfk_2`
    FOREIGN KEY (`parent_id`)
    REFERENCES `gitcommit`.`commits` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`followers` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`followers` (
  `follower_id` INT(11) NOT NULL COMMENT '',
  `user_id` INT(11) NOT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  PRIMARY KEY (`follower_id`, `user_id`)  COMMENT '',
  CONSTRAINT `follower_fk1`
    FOREIGN KEY (`follower_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `follower_fk2`
    FOREIGN KEY (`user_id`)
    REFERENCES `gitcommit`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`pull_requests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`pull_requests` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`pull_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `head_repo_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `base_repo_id` INT(11) NOT NULL COMMENT '',
  `head_commit_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `base_commit_id` INT(11) NOT NULL COMMENT '',
  `pullreq_id` INT(11) NOT NULL COMMENT '',
  `intra_branch` TINYINT(1) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  CONSTRAINT `pull_requests_ibfk_1`
    FOREIGN KEY (`head_repo_id`)
    REFERENCES `gitcommit`.`projects` (`id`),
  CONSTRAINT `pull_requests_ibfk_2`
    FOREIGN KEY (`base_repo_id`)
    REFERENCES `gitcommit`.`projects` (`id`),
  CONSTRAINT `pull_requests_ibfk_3`
    FOREIGN KEY (`head_commit_id`)
    REFERENCES `gitcommit`.`commits` (`id`),
  CONSTRAINT `pull_requests_ibfk_4`
    FOREIGN KEY (`base_commit_id`)
    REFERENCES `gitcommit`.`commits` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`issues`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`issues` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`issues` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `reporter_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `assignee_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `pull_request` TINYINT(1) NOT NULL COMMENT '',
  `pull_request_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `issue_id` INT(11) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  CONSTRAINT `issues_ibfk_1`
    FOREIGN KEY (`repo_id`)
    REFERENCES `gitcommit`.`projects` (`id`),
  CONSTRAINT `issues_ibfk_2`
    FOREIGN KEY (`reporter_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `issues_ibfk_3`
    FOREIGN KEY (`assignee_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `issues_ibfk_4`
    FOREIGN KEY (`pull_request_id`)
    REFERENCES `gitcommit`.`pull_requests` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `gitcommit`.`organization_members`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`organization_members` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`organization_members` (
  `org_id` INT(11) NOT NULL COMMENT '',
  `user_id` INT(11) NOT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  PRIMARY KEY (`org_id`, `user_id`)  COMMENT '',
  CONSTRAINT `organization_members_ibfk_1`
    FOREIGN KEY (`org_id`)
    REFERENCES `gitcommit`.`users` (`id`),
  CONSTRAINT `organization_members_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `gitcommit`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`pull_request_commits`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`pull_request_commits` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`pull_request_commits` (
  `pull_request_id` INT(11) NOT NULL COMMENT '',
  `commit_id` INT(11) NOT NULL COMMENT '',
  PRIMARY KEY (`pull_request_id`, `commit_id`)  COMMENT '',
  CONSTRAINT `pull_request_commits_ibfk_1`
    FOREIGN KEY (`pull_request_id`)
    REFERENCES `gitcommit`.`pull_requests` (`id`),
  CONSTRAINT `pull_request_commits_ibfk_2`
    FOREIGN KEY (`commit_id`)
    REFERENCES `gitcommit`.`commits` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `gitcommit`.`pull_request_history`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gitcommit`.`pull_request_history` ;

CREATE TABLE IF NOT EXISTS `gitcommit`.`pull_request_history` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `pull_request_id` INT(11) NOT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `action` VARCHAR(255) NOT NULL COMMENT '',
  `actor_id` INT(11) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  CONSTRAINT `pull_request_history_ibfk_1`
    FOREIGN KEY (`pull_request_id`)
    REFERENCES `gitcommit`.`pull_requests` (`id`),
  CONSTRAINT `pull_request_history_ibfk_2`
    FOREIGN KEY (`actor_id`)
    REFERENCES `gitcommit`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
