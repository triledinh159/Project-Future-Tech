# Table of content
- [Project Future Tech](#project-future-tech)

---

## Project Future Tech
Application for **AWS Build on Vietnam** 2022 event:
Solution for ZaloPay's Challenge

Author: MasterYuri
### 1) Problems
The challenge: As adoption of cashless transactions in Vietnam continues to grow, please propose a solution & develop a feature for a mobile wallet that enables its users to pay for parking more conveniently.

 When we recieved the challenge, we recognized that main key the judges wanted to give the contestants is "**MORE CONVENIENTLY**". So that, we decided to choose "**NFC technology**", which is the best way(I think) to make a more conveniently transaction in retail sectors and some companies as Samsung or Apple are developing that technology.
 
 Bunch of information was found give me some questions: 
* First is "Why this tech is not popular in specific: Vietnam".
* Second is "Why don't we inheritage it cuz Samsung have Samsung Pay, Apple have Apple Pay which are strongly being developed in non-cash payment".
 
 Then we believed that this tech must not be wasted!
###  2) Solution
We split this challenge into 3 parts: Basic architecture, backend, frontend.
*  **Basic architecture**: We decided to build a plan, which services would be used and the effect. we had create DFD first to develop AWS architecture to visualize not only backend but also frontend.![](https://i.imgur.com/BNDGoKg.png)![](https://i.imgur.com/MoUUQZK.png)
![](https://i.imgur.com/zf6RtN8.png)

*  **Backend**: After we had Basic architecture, we can easily find the way out to figure the construction of the backend which AWS services in simple way: AWS lambda, S3 bucket, DynamoDB, Amazon Rekognition.
*  **Frontend**: We had build the app which can read NFC signal.![](https://i.imgur.com/xPVfW4G.jpg)

### 3) Result
With our solution, we were luckily chosen to be qualified to the finale of AWS Build on Vietnam and the solution was chosen to be the Best Technicality.
