# Table of content
- [Project Future Tech](#project-future-tech)

---

## Project Future Tech

Application for **AWS Build on Vietnam 2022** event: 
Solution for ZaloPay's Challenge https://www.buildonvietnam.com/

Author: MasterYuri 
### 1) Problems
The challenge: As the adoption of cashless transactions in Vietnam continues to grow, please propose a solution & develop a feature for a mobile wallet that enables users to pay for parking more conveniently.

 When we received the challenge, we recognized that the primary key the judges wanted to give the contestants was "**MORE CONVENIENTLY**". So, we decided to choose "**NFC technology**", which is the best way(I think) to make a more convenient transaction in retail sectors, and some companies such as Samsung or Apple are developing that technology.
 
 A bunch of information was found gave me some questions: 
* First is "Why this tech is not popular in specific: Vietnam".
* Second is "Why don't we inherit it cuz Samsung has Samsung Pay, Apple has Apple Pay which is strongly being developed in non-cash payment".
 
 Then we believed that this tech must not be wasted!
###  2) Solution
We split this challenge into 3 parts: Basic architecture, backend, and frontend.
*  **Basic architecture**: We decided to build a plan, on which services would be used and the effect. we had to create DFD first to develop AWS architecture to visualize the backend.![DFDLv1](https://github.com/triledinh159/Project-Future-Tech/assets/91708260/c08ca539-b3a1-4e5b-a561-2df59b73de99)



*  **Backend**: After we had Basic architecture, we could easily find a way out to figure out the construction of the backend which AWS services in a simple way: AWS lambda, S3 bucket, DynamoDB, and Amazon Rekognition.![](https://i.imgur.com/MoUUQZK.png)
![](https://i.imgur.com/zf6RtN8.png)
*  **Frontend**: We had built an app that can read NFC signals.![](https://i.imgur.com/xPVfW4G.jpg)

### 3) Result
With our solution, we were luckily chosen to be qualified for the finale of AWS Build on Vietnam and the solution was chosen to be the [Best Technicality](./AWSLambda/cert/tech.pdf).
Here is the Demo link: https://youtu.be/hi772lhfCak
