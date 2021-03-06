/*
 * Signs a digest (Digest and sign are done separately)
 * ToraNova 2019 aug 14
 * gcc 9.1.0
 * gcc sign.c -o sign -lcrypto
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/pem.h>

int main(int argc, char *argv[]){

	//declare vars
	EVP_PKEY *pkey = NULL;
	EVP_MD_CTX *mdctx = EVP_MD_CTX_create();
	const EVP_MD *md = EVP_sha512(); //sha512

	//result codes
	int rc;
	unsigned int d_size, i;
	size_t s_size;
	unsigned char d_message[EVP_MAX_MD_SIZE];
	unsigned char *s_message = NULL;

	//target message
	char message[] = "Hello World";

	//open file stream
	if(argv[1] == NULL){
		printf("Please specify private key file.\n");
		exit(1);
	}
	FILE *fptr = fopen( argv[1], "r" );

	//reads the private key for signing
	pkey = PEM_read_PrivateKey( fptr, &pkey , NULL, NULL);

	//hashing the message, output in d_message with size d_size
	rc = EVP_Digest( message, strlen(message), d_message, &d_size, md, NULL);

	//initialize the signing
	rc = EVP_DigestSignInit(mdctx, NULL, NULL, NULL, pkey);

	/*
	 * This area seesm to throw segmentation fault when using secret keys
	 * generated by bouncy's castle ed25519 keygen
	 * we truncate off the appended public key on bouncy castle's generated pkcs8
	 * private keys to possibly go around this issue
	 */
	//using this to obtain length of signature (empty signature NULL)
	rc = EVP_DigestSign(mdctx, NULL, &s_size, d_message, d_size);
	s_message = (unsigned char *) malloc( s_size );

	//actual sign
	rc = EVP_DigestSign( mdctx, s_message, &s_size, d_message, d_size);

	//cleanup
	EVP_MD_CTX_free(mdctx);
	fclose(fptr);

	//output
	for (i = 0; i < s_size; i++)
	printf("%02x", s_message[i]);
	printf("\n");
}
