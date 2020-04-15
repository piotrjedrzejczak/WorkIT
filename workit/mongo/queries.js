// Get Unique Cities, count occurances and sort descending.

db.offers.aggregate(
    [
        {
            $group: {
                _id: { city: "$city" },
                count: { $sum: 1 }
            }
        },
        { $sort: { count: -1}}
    ]
)

// Get all documents

db.offers.find()