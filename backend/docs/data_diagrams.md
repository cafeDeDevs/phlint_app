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
        int user_id FK
        string title
        string s3_url
        bool isPrivate
    }
    PHOTOS {
        int id PK
        int album_id FK
        string date
        string s3_url
    }
    USER ||--o{ NETWORKS: has
    NETWORKS {
        int id PK
        int founder_id FK
        int user_id FK
        int album_id FK
    }
    NETWORKS }o -- |{ ALBUMS: accesses
</pre>
</div>
