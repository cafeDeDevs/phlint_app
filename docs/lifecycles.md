**SignUp**

Signing Up is usually initialized by invitation from one of our existing Users.
Upon invitation, the Potential User is Onboarded through
a standard Invitation Email and Sign Up Process. It is expected that the User
who Invited the Potential User has done so in order to grant them access to a
particular Album via a Network. This process is also reflective of how one
User of the Application can invite another User to join a Network and view
said Network's Album (maybe minus the email verification part?).

<div align="center">
<pre class="mermaid">
journey
    title SignUp/Join (happy path)
    section Invite John
      Clicks On "Invite" Button: 4: Me
    section Request Network
      Send Invitation Email: 3: Application
      Accept Invitation: 4: John
    section SignUp
      Redirect Back to App: 3: Application
      Sign Up For App: 4: John, Application
    section Join First Network
      Sign Up John For App: 3: Application
      Join John To My Network: 3: Application
      Redirect John To My Album: 5: Me, John
</pre>
</div>

**Upload Image**

NOTE: This diagram illustrates an initial implementation where the image is
encrypted on the <em>server</em>. Should performance become an issue, this
implementation will need to be rethought using Web Assembly, where encryption
will occur on the <em>client</em>.

<div align="center">
<pre class="mermaid">
journey
    title Upload Image (happy path)
    section User Uploads Image
      Clicks On "Upload Image" Button: 3: Client
    section Upload Raw Image
      Raw Image Is Uploaded To Server: 3: Client
      Server Confirms Receipt Of Raw Image: 3: Server
    section Server Proccesses Image
      Server Uses AES Script to Encrypt Image: 3: Server
      Raw Image Is Cached For User To View Immediately: 3: Server, Cache
      Cached Raw Image Is Sent Back To User: 3: Server, Cache, Client
      Server Logs Image MetaData In PostgreSQL DB: 3: Server, DB
      Server Sends Encrypted Image to S3 Bucket: 3: Server, S3
</pre>
</div>

**Request Image**

NOTE: This diagram illustrates an initial implementation where the image is
decrypted on the <em>server</em>. Should performance become an issue, this
implementation will need to be rethought using Web Assembly, where decryption
will occur on the <em>client</em>.

<div align="center">
<pre class="mermaid">
journey
    title Request Image (happy path)
    section User Requests Image
      Clicks On "View Image" Button: 3: Client
      Client Sends Permissions Credentials (JWT): 3: Client
    section Server Procceses Request
      Server Checks Client's Credentials against PostgreSQL DB: 3: Server, DB
      Server Receives S3 bucket address of encrypted image: Server, DB, S3
      S3 Sends Encrypted Image to Server: 3: S3, Server
      Server Decrypts Image Using AES script: Server
      Server Sends Raw Image to Client: Server, Client
    section Server Proccesses Image
      Server Uses AES Script to Encrypt Image: 3: Server
      Raw Image Is Cached For User To View Immediately: 3: Server, Cache
    section Client Receives Raw Image
      Client Views Raw Image: 3: Client
</pre>
</div>
