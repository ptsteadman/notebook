### Upgrading OroCrm from 1.4 to 1.8

Instructions here:
https://github.com/orocrm/crm-application/blob/master/UPGRADE.md

The first issue I ran into was that there were a few modifications to files in
the `/var/www/html/vendor/oro/crm/src/OroCrm/Bundle/TestFrameworkBundle`
directory, which made it impossible to successfully run the `php composer.phar
update` command, because composer can't check out the new version of the OroCrm
repository.  There's also a `/var/www/html/src/OroCrm/Bundle` directory, which
caused some confusion.  It seems that this latter directory is where the
consultant installed the extensions.  I'm not sure how those changes to the
TestFrameworkBundle occured, but I git stashed them and then I was able to run
the composer dependency upgrade step.

Then I attempted to run the `php app/console oro:platform:update --env=prod` as
specified in the Upgrade instructions.  However, one needs to add the `--force`
argument to the update command.  I'm notsure why that's not in the upgrade
documentation.

I ran into some issues in migrating the tables used for the zendesk integration.
The update script was trying to create the tables, but they were already there
(but all empty).  I backed up the database, deleted the tables, and this solved
that problem.

Then I ran into this error: 

```
OroCRM\Bundle\MagentoBundle\Migrations\Data\ORM\LoadNewsletterSubscriberStatusData
[Doctrine\Common\Persistence\Mapping\MappingException]
Class ‘Extend\Entity\EV_Mage_Subscr_Status’ does not exist
```
Forum Thread:
http://www.orocrm.com/forums/topic/mappingexception-class-extendentityev_mage_subscr_status-does-not-exist
