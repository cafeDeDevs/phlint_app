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
