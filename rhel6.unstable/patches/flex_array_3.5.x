diff --git a/ldms/src/core/ldms.h b/ldms/src/core/ldms.h
index 952f43c..5328f8d 100644
--- a/ldms/src/core/ldms.h
+++ b/ldms/src/core/ldms.h
@@ -583,7 +583,7 @@ typedef struct ldms_dir_s {
 	int set_count;
 
 	/** each string is null terminated. */
-	char *set_names[0];
+	char *set_names[/*flex*/];
 } *ldms_dir_t;
 
 typedef void (*ldms_dir_cb_t)(ldms_t t, int status, ldms_dir_t dir, void *cb_arg);
@@ -1407,7 +1407,7 @@ typedef struct ldms_notify_event_s {
 %immutable;
 #endif
 	size_t len;		/*! The size of the event in bytes */
-	unsigned char u_data[0];/*! User-data for the LDMS_USER_DATA
+	unsigned char u_data[/*flex*/];/*! User-data for the LDMS_USER_DATA
 				  type */
 } *ldms_notify_event_t;
 
diff --git a/ldms/src/core/ldms_core.h b/ldms/src/core/ldms_core.h
index c2e7d54..943a749 100644
--- a/ldms/src/core/ldms_core.h
+++ b/ldms/src/core/ldms_core.h
@@ -98,7 +98,7 @@ typedef struct ldms_value_desc {
 %immutable;
 #endif
 	uint8_t vd_name_len;	/*! The length of the metric name in bytes*/
-	char vd_name[0];	/*! The metric name */
+	char vd_name[/*flex*/];	/*! The metric name */
 } *ldms_mdesc_t;
 #pragma pack()
 
@@ -177,7 +177,7 @@ struct ldms_set_hdr {
 	uint32_t card;		/* Size of dictionary */
 	uint32_t meta_sz;	/* size of meta data in bytes */
 	uint32_t data_sz;	/* size of metric values in bytes */
-	uint32_t dict[0];	/* The attr/metric dictionary */
+	uint32_t dict[/*flex*/];	/* The attr/metric dictionary */
 };
 
 /**
@@ -246,7 +246,7 @@ typedef struct ldms_name {
 %immutable;
 #endif
 	uint8_t len;
-	char name[0];
+	char name[/*flex*/];
 } *ldms_name_t;
 
 #ifndef roundup
diff --git a/ldms/src/core/ldms_xprt.h b/ldms/src/core/ldms_xprt.h
index 5b7aff4..326f770 100644
--- a/ldms/src/core/ldms_xprt.h
+++ b/ldms/src/core/ldms_xprt.h
@@ -141,7 +141,7 @@ struct ldms_send_cmd_param {
 %immutable;
 #endif
 	uint32_t msg_len;
-	char msg[0];
+	char msg[/*flex*/];
 };
 
 struct ldms_lookup_cmd_param {
@@ -199,7 +199,7 @@ struct ldms_rendezvous_lookup_param {
 %immutable;
 #endif
 	uint32_t inst_name_len;
-	char schema_inst_name[0]; /* schema name and then instance name */
+	char schema_inst_name[/*flex*/]; /* schema name and then instance name */
 };
 
 struct ldms_rendezvous_push_param {
@@ -246,7 +246,7 @@ struct ldms_dir_reply {
 %immutable;
 #endif
 	uint32_t set_list_len;
-	char set_list[0];
+	char set_list[/*flex*/];
 };
 
 struct ldms_req_notify_reply {
@@ -265,7 +265,7 @@ struct ldms_push_reply {
 	uint32_t flags;
 	uint32_t data_off;
 	uint32_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 struct ldms_reply_hdr {
diff --git a/ldms/src/ldmsd/ldmsd_request.h b/ldms/src/ldmsd/ldmsd_request.h
index efa9a94..7cb66bc 100644
--- a/ldms/src/ldmsd/ldmsd_request.h
+++ b/ldms/src/ldmsd/ldmsd_request.h
@@ -189,7 +189,7 @@ typedef struct ldmsd_req_attr_s {
 	uint32_t discrim;	/* If 0, end of attr_list */
 	uint32_t attr_id;	/* Attribute identifier, unique per ldmsd_req_hdr_s.cmd_id */
 	uint32_t attr_len;	/* Size of value in bytes */
-	uint8_t attr_value[0];	/* Size is attr_len */
+	uint8_t attr_value[/*flex*/];	/* Size is attr_len */
 } *ldmsd_req_attr_t;
 
 /**
diff --git a/ldms/src/sampler/lustre/lustre_sampler.h b/ldms/src/sampler/lustre/lustre_sampler.h
index 1f5cbdd..c31f11f 100644
--- a/ldms/src/sampler/lustre/lustre_sampler.h
+++ b/ldms/src/sampler/lustre/lustre_sampler.h
@@ -238,7 +238,7 @@ struct lustre_svc_stats {
 	int mh_status_idx;
 	ldms_set_t set;
 	int mlen;
-	struct lustre_metric_ctxt mctxt[0];
+	struct lustre_metric_ctxt mctxt[/*flex*/];
 };
 
 /**
diff --git a/ldms/src/store/store_flatfile.c b/ldms/src/store/store_flatfile.c
index e651699..62f2421 100644
--- a/ldms/src/store/store_flatfile.c
+++ b/ldms/src/store/store_flatfile.c
@@ -96,7 +96,7 @@ struct flatfile_store_instance {
 	idx_t ms_idx;
 	LIST_HEAD(ms_list, flatfile_metric_store) ms_list;
 	int metric_count;
-	struct flatfile_metric_store *ms[0];
+	struct flatfile_metric_store *ms[/*flex*/];
 };
 
 static pthread_mutex_t cfg_lock;
diff --git a/lib/src/coll/idx_priv.h b/lib/src/coll/idx_priv.h
index d496de2..040443b 100644
--- a/lib/src/coll/idx_priv.h
+++ b/lib/src/coll/idx_priv.h
@@ -69,7 +69,7 @@ struct idx_entry_s {
 struct idx_layer_s {
 	int obj_count;			/* objs in this layer. */
 	int layer_count;		/* sub-layers below this layer */
-	struct idx_entry_s entries[0];	/* table of entries if we are a leaf */
+	struct idx_entry_s entries[/*flex*/];	/* table of entries if we are a leaf */
 };
 
 #endif
diff --git a/lib/src/coll/str_map.c b/lib/src/coll/str_map.c
index e2a39d2..a7a46d5 100644
--- a/lib/src/coll/str_map.c
+++ b/lib/src/coll/str_map.c
@@ -72,7 +72,7 @@
  */
 struct str_map {
 	size_t hash_size; /**< hash size */
-	struct obj_list_head lh_table[0]; /**< hash table */
+	struct obj_list_head lh_table[/*flex*/]; /**< hash table */
 };
 
 struct str_map* str_map_create(size_t sz)
diff --git a/lib/src/ovis_event/ovis_event_priv.h b/lib/src/ovis_event/ovis_event_priv.h
index 69a471b..53804c6 100644
--- a/lib/src/ovis_event/ovis_event_priv.h
+++ b/lib/src/ovis_event/ovis_event_priv.h
@@ -71,7 +71,7 @@ struct ovis_event {
 struct ovis_event_heap {
 	uint32_t alloc_len;
 	uint32_t heap_len;
-	struct ovis_event *ev[0];
+	struct ovis_event *ev[/*flex*/];
 };
 
 struct ovis_event_manager {
diff --git a/lib/src/ovis_util/util.h b/lib/src/ovis_util/util.h
index 6d895b7..c2d5a3f 100644
--- a/lib/src/ovis_util/util.h
+++ b/lib/src/ovis_util/util.h
@@ -111,7 +111,7 @@ struct attr_value_list {
 	int size;
 	int count;
 	LIST_HEAD(string_list, string_ref_s) strings;
-	struct attr_value list[0];
+	struct attr_value list[/*flex*/];
 };
 
 /**
diff --git a/lib/src/zap/rdma/zap_rdma.h b/lib/src/zap/rdma/zap_rdma.h
index a5e5be5..3131b1c 100644
--- a/lib/src/zap/rdma/zap_rdma.h
+++ b/lib/src/zap/rdma/zap_rdma.h
@@ -83,19 +83,19 @@ struct z_rdma_share_msg {
 	uint32_t len;
 	uint32_t rkey;
 	uint64_t va;
-	char msg[0];
+	char msg[/*flex*/];
 };
 
 struct z_rdma_accept_msg {
 	struct z_rdma_message_hdr hdr;
 	uint32_t len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 struct z_rdma_reject_msg {
 	struct z_rdma_message_hdr hdr;
 	uint32_t len;
-	char msg[0];
+	char msg[/*flex*/];
 };
 
 #pragma pack()
@@ -135,7 +135,7 @@ struct z_rdma_context {
 struct z_rdma_conn_data {
 	struct zap_version v;
 	uint8_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 #pragma pack(pop)
 
diff --git a/lib/src/zap/sock/zap_sock.h b/lib/src/zap/sock/zap_sock.h
index f1edde9..bde671d 100644
--- a/lib/src/zap/sock/zap_sock.h
+++ b/lib/src/zap/sock/zap_sock.h
@@ -153,7 +153,7 @@ struct sock_msg_connect {
 	struct zap_version ver;
 	char sig[8];
 	uint32_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 /**
@@ -162,7 +162,7 @@ struct sock_msg_connect {
 struct sock_msg_sendrecv {
 	struct sock_msg_hdr hdr;
 	uint32_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 /**
@@ -183,7 +183,7 @@ struct sock_msg_read_resp {
 	uint16_t status; /**< Return status */
 	uint64_t dst_ptr; /**< Destination memory addr (on initiator) */
 	uint32_t data_len; /**< Response data length */
-	char data[0]; /**< Response data */
+	char data[/*flex*/]; /**< Response data */
 };
 
 /**
@@ -194,7 +194,7 @@ struct sock_msg_write_req {
 	uint32_t dst_map_key; /**< Destination map key */
 	uint64_t dst_ptr; /**< Destination address */
 	uint32_t data_len; /**< Data length */
-	char data[0]; /**< data for SOCK_MSG_WRITE_REQ */
+	char data[/*flex*/]; /**< data for SOCK_MSG_WRITE_REQ */
 };
 
 /**
@@ -214,7 +214,7 @@ struct sock_msg_rendezvous {
 	uint32_t acc; /**< Access */
 	uint64_t addr; /**< Address in the map */
 	uint32_t data_len; /**< Length */
-	char msg[0]; /**< Context */
+	char msg[/*flex*/]; /**< Context */
 };
 
 /**
diff --git a/lib/src/zap/ugni/zap_ugni.h b/lib/src/zap/ugni/zap_ugni.h
index 9c13a7f..f45733d 100644
--- a/lib/src/zap/ugni/zap_ugni.h
+++ b/lib/src/zap/ugni/zap_ugni.h
@@ -226,7 +226,7 @@ struct zap_ugni_msg_hdr {
 struct zap_ugni_msg_regular {
 	struct zap_ugni_msg_hdr hdr;
 	uint32_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 /**
@@ -238,7 +238,7 @@ struct zap_ugni_msg_rendezvous {
 	zap_access_t acc;
 	uint64_t addr; /**< Address in the map */
 	uint32_t data_len; /**< Length */
-	char msg[0]; /**< Context */
+	char msg[/*flex*/]; /**< Context */
 };
 
 /**
@@ -249,7 +249,7 @@ struct zap_ugni_msg_accepted {
 	uint32_t inst_id; /**< inst_id of the accepter (passive side). */
 	uint32_t pe_addr; /**< peer address of the accepter (passive side). */
 	uint32_t data_len;
-	char data[0];
+	char data[/*flex*/];
 };
 
 static char ZAP_UGNI_SIG[8] = "UGNI";
@@ -265,7 +265,7 @@ struct zap_ugni_msg_connect {
 	uint32_t inst_id; /**< inst_id of the requester (active side). */
 	uint32_t pe_addr; /**< peer address of the requester (active side). */
 	uint32_t data_len; /**< Connection data*/
-	char data[0];      /**< Size of connection data */
+	char data[/*flex*/];      /**< Size of connection data */
 };
 
 #pragma pack()
diff --git a/lib/src/zap/zap.c b/lib/src/zap/zap.c
index 41662a6..9f148f6 100644
--- a/lib/src/zap/zap.c
+++ b/lib/src/zap/zap.c
@@ -299,7 +299,7 @@ void blocking_zap_cb(zap_ep_t zep, zap_event_t ev)
 
 struct zap_interpose_ctxt {
 	struct zap_event ev;
-	unsigned char data[0];
+	unsigned char data[/*flex*/];
 };
 
 /*
