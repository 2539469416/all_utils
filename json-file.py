import json

str = """"
 games: [{
            id: 1,
            type: "pc",
            game: "加拿大28",
            gameid: 1,
            roomid: 1,
            open: !1,
            order: 1,
            online: "",
            icon: ""
        }, {
            id: 2,
            type: "pc",
            game: "加拿大28高赔率",
            gameid: 1,
            roomid: 2,
            open: !1,
            order: 2,
            online: "",
            icon: ""
        }, {
            id: 3,
            type: "pc",
            game: "加拿大28高赔率3",
            gameid: 1,
            roomid: 3,
            open: !1,
            order: 3,
            online: "",
            icon: ""
        }, {
            id: 4,
            type: "pc",
            game: "加拿大28高赔率4",
            gameid: 1,
            roomid: 4,
            open: !1,
            order: 4,
            online: "",
            icon: ""
        }, {
            id: 5,
            type: "pc",
            game: "极速28",
            gameid: 3,
            roomid: 1,
            open: !1,
            order: 7,
            online: "",
            icon: ""
        }, {
            id: 6,
            type: "pc",
            game: "极速28高赔率",
            gameid: 3,
            roomid: 2,
            open: !1,
            order: 8,
            online: "",
            icon: ""
        }, {
            id: 7,
            type: "pc",
            game: "极速28高赔率3",
            gameid: 3,
            roomid: 3,
            open: !1,
            order: 8,
            online: "",
            icon: ""
        }, {
            id: 8,
            type: "pc",
            game: "极速28高赔率4",
            gameid: 3,
            roomid: 4,
            open: !1,
            order: 8,
            online: "",
            icon: ""
        }, {
            id: 9,
            type: "pc",
            game: "宾果28",
            gameid: 4,
            roomid: 1,
            open: !1,
            order: 9,
            online: "",
            icon: ""
        }, {
            id: 10,
            type: "pc",
            game: "宾果28高赔率",
            gameid: 4,
            roomid: 2,
            open: !1,
            order: 10,
            online: "",
            icon: ""
        }, {
            id: 11,
            type: "pc",
            game: "宾果28高赔率3",
            gameid: 4,
            roomid: 3,
            open: !1,
            order: 10,
            online: "",
            icon: ""
        }, {
            id: 12,
            type: "pc",
            game: "宾果28高赔率4",
            gameid: 4,
            roomid: 4,
            open: !1,
            order: 10,
            online: "",
            icon: ""
        }, {
            id: 13,
            type: "pc",
            game: "分分28",
            gameid: 5,
            roomid: 1,
            open: !1,
            order: 11,
            online: "",
            icon: ""
        }, {
            id: 14,
            type: "pc",
            game: "分分28高赔率",
            gameid: 5,
            roomid: 2,
            open: !1,
            order: 12,
            online: "",
            icon: ""
        }, {
            id: 15,
            type: "pc",
            game: "分分28高赔率3",
            gameid: 5,
            roomid: 3,
            open: !1,
            order: 12,
            online: "",
            icon: ""
        }, {
            id: 16,
            type: "pc",
            game: "分分28高赔率4",
            gameid: 5,
            roomid: 4,
            open: !1,
            order: 12,
            online: "",
            icon: ""
        }, {
            id: 17,
            type: "pc",
            game: "PC蛋蛋幸运28",
            gameid: 6,
            roomid: 1,
            open: !1,
            order: 13,
            online: "",
            icon: ""
        }, {
            id: 18,
            type: "pc",
            game: "PC蛋蛋幸运28高赔率",
            gameid: 6,
            roomid: 2,
            open: !1,
            order: 14,
            online: "",
            icon: ""
        }, {
            id: 19,
            type: "pc",
            game: "PC蛋蛋幸运28高赔率3",
            gameid: 6,
            roomid: 3,
            open: !1,
            order: 14,
            online: "",
            icon: ""
        }, {
            id: 20,
            type: "pc",
            game: "PC蛋蛋幸运28高赔率4",
            gameid: 6,
            roomid: 4,
            open: !1,
            order: 14,
            online: "",
            icon: ""
        }, {
            id: 20.1,
            type: "pc",
            game: "俄罗斯28",
            gameid: 7,
            roomid: 1,
            open: !1,
            order: 27,
            online: "",
            icon: ""
        }, {
            id: 20.2,
            type: "pc",
            game: "俄罗斯28高赔率2",
            gameid: 7,
            roomid: 2,
            open: !1,
            order: 28,
            online: "",
            icon: ""
        }, {
            id: 20.3,
            type: "pc",
            game: "俄罗斯28高赔率3",
            gameid: 7,
            roomid: 3,
            open: !1,
            order: 29,
            online: "",
            icon: ""
        }, {
            id: 20.4,
            type: "pc",
            game: "俄罗斯28高赔率4",
            gameid: 7,
            roomid: 4,
            open: !1,
            order: 30,
            online: "",
            icon: ""
        }, {
            id: 20.5,
            type: "pc",
            game: "澳大利亚28",
            gameid: 8,
            roomid: 1,
            open: !1,
            order: 31,
            online: "",
            icon: ""
        }, {
            id: 20.6,
            type: "pc",
            game: "澳大利亚28高赔率2",
            gameid: 8,
            roomid: 2,
            open: !1,
            order: 32,
            online: "",
            icon: ""
        }, {
            id: 20.7,
            type: "pc",
            game: "澳大利亚28高赔率3",
            gameid: 8,
            roomid: 3,
            open: !1,
            order: 33,
            online: "",
            icon: ""
        }, {
            id: 20.8,
            type: "pc",
            game: "澳大利亚28高赔率4",
            gameid: 8,
            roomid: 4,
            open: !1,
            order: 34,
            online: "",
            icon: ""
        }, {
            id: 21,
            type: "pk10",
            game: "澳洲幸运10",
            gameid: 1002,
            roomid: 1,
            open: !1,
            order: 16,
            online: "",
            icon: ""
        }, {
            id: 22,
            type: "pk10",
            game: "幸运飞艇API68",
            gameid: 1003,
            roomid: 1,
            open: !1,
            order: 17,
            online: "",
            icon: ""
        }, {
            id: 23,
            type: "pk10",
            game: "极速赛车",
            gameid: 1004,
            roomid: 1,
            open: !1,
            order: 18,
            online: "",
            icon: ""
        }, {
            id: 24,
            type: "pk10",
            game: "极速飞艇",
            gameid: 1005,
            roomid: 1,
            open: !1,
            order: 19,
            online: "",
            icon: ""
        }, {
            id: 25,
            type: "k3",
            game: "极速快3",
            gameid: 2004,
            roomid: 1,
            open: !1,
            order: 23,
            online: "",
            icon: ""
        }, {
            id: 26,
            type: "ssc",
            game: "极速时时彩",
            gameid: 3002,
            roomid: 1,
            open: !1,
            order: 25,
            online: "",
            icon: ""
        }, {
            id: 27,
            type: "ssc",
            game: "澳洲幸运5",
            gameid: 3003,
            roomid: 1,
            open: !1,
            order: 26,
            online: "",
            icon: ""
        }]]
        """
print(json.loads(str))