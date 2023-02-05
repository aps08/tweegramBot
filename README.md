![banner](./docs/images/banner.png)
<p align="center">
    <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" alt="vscode">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter">
    <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</p>

# tweegramBot
A semi-configured respository, which help you convert your telegram messages to twitter tweets, also retweet the tweets tweeted by specific list of users.

## Notes
* One time manual setup is required, to create the `*.session` file, for telegram operations.
* It is recommended to not keep the repository in public, with the `*.session`, which was created in the first step, and `*.json` file which will be created when you add users to your list.

## How to use
1. Get your API secrets for telegram from [here](https://my.telegram.org/apps).
2. Get your API secrets for twitter from [here](https://developer.twitter.com/en/portal/dashboard).
3. Fork this reposiotry, and uncomment the commented lines in [this](https://github.com/aps08/teltotwt/blob/main/.github/workfows/actions.yml) file.
4. Create secrets for this repository. Total 8 secret key-value pair need to be created, 6 of them would be the API secrets, 1 would be telegram group/user name and 1 would be your github email. You can see the keys and instructions in [this](https://github.com/aps08/teltotwt/blob/main/src/config.py) file.
5. Once the above steps are completed, this repo will run everyday at mid-night, and convert all your telegram messages into tweets.
 
<br>
<p align="center">
 <a href="https://twitter.com/aps08__"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white"></a>
 <a href="https://medium.com/@aps08"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white"></a>
 <a href="https://www.linkedin.com/in/aps08"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
 <a href="https://github.com/aps08"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>
 <a href="https://www.youtube.com/channel/UC8biJQnoqm1s2FZ8LK90baA"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
 <a href="mailto:anoopprsingh@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"></a>
</p>
