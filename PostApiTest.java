package com.training;
import io.restassured.RestAssured;
import org.junit.jupiter.api.*;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class PostsApiTest {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "https://jsonplaceholder.typicode.com";
    }

    @Test
    void getPost() {
        given().when().get("/posts/1")
                .then().statusCode(200)
                .body("id", notNullValue())
                .body("title", notNullValue());
    }

    @Test
    void createPost() {
        given().contentType("application/json")
                .body("{\"title\":\"Postman E2E Test Post\",\"body\":\"created by test\",\"userId\":1}")
                .when().post("/posts")
                .then().statusCode(201)
                .body("id", notNullValue());
    }

    @Test
    void updatePost() {
        given().contentType("application/json")
                .body("{\"id\":1,\"title\":\"Updated Title\",\"body\":\"Updated content\",\"userId\":1}")
                .when().put("/posts/1")
                .then().statusCode(200)
                .body("title", equalTo("Updated Title"));
    }

    @Test
    void deletePost() {
        given().when().delete("/posts/1")
                .then().statusCode(200);
    }

    @Test
    void getNonExistentPost_shouldReturn404() {
        given().when().get("/posts/99999")
                .then().statusCode(404);
    }
}