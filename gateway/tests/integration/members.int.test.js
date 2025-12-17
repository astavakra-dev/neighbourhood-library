// tests/integration/members.int.test.js
const request = require("supertest");
const app = require("../../src/index");

jest.mock("../../src/grpc/client", () => ({
  AddMember: (body, cb) => cb(null, { id: 99, ...body })
}));

describe("Members integration", () => {
  it("should add a member", async () => {
    const res = await request(app).post("/members").send({
      name: "Alice",
      phone: "1234567890",
      email: "alice@example.com"
    });
    expect(res.status).toBe(200);
    expect(res.body.id).toBe(99);
  });

  it("should reject invalid member payload", async () => {
    const res = await request(app).post("/members").send({
      name: "Bob",
      phone: "12ab",
      email: "not-an-email"
    });
    expect(res.status).toBe(400);
  });
});