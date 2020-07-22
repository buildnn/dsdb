db.createUser(
    {
        user: "dsdbuser",
        pwd: "dsdbpass",
        roles: [
            {
                role: "readWrite",
                db:"dsdb"
            }
        ]
    }
)