## Data Diagrams For Photo Share App

**User To Photos Data Pipeline**

Each of our Users holds two roles within the context of our application. One of
being the Owner of many albums, as well as a Member of various Networks where
another User is the Owner of said Network. This Network grants access to
an Album, which holds reference to various Photos.

Note that the a User having
access to an Albums via being part of a Network <em>is optional</em>, as the
Album Table has a boolean `isPrivate` field that if `false`, means that the
Network Table is <em>not</em> checked.

<div align="center">
<pre class="mermaid">
    erDiagram
    USER ||--o{ ALBUMS : owns
    USER {
        int id PK
        string name
        string email
    }
    ALBUMS ||--|{ PHOTOS : contains
    ALBUMS {
        int id PK
        int userId FK
        string title
        string locationUrlOrDirectory
        bool isPrivate
    }
    PHOTOS {
        int id PK
        int albumId FK
        string date
        string locationUrlOrDirectory
    }
    USER ||--o{ NETWORKS: has
    NETWORKS {
        int id PK
        int founderId FK
        int userId FK
        int albumId FK
    }
    NETWORKS }o -- |{ ALBUMS: accesses
</pre>
</div>

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
