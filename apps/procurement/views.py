from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import PurchaseOrderFilter
from .models import PurchaseOrder, PurchaseOrderStatus
from .permissions import (
    CanApprovePurchaseOrders,
    CanCompletePurchaseOrders,
    CanManagePurchaseOrders,
)
from .serializers import PurchaseOrderSerializer, PurchaseOrderStatusSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = (
        PurchaseOrder.objects.select_related(
            "supplier",
            "created_by",
            "approved_by",
        )
        .prefetch_related("items__product")
        .all()
    )
    serializer_class = PurchaseOrderSerializer
    permission_classes = [CanManagePurchaseOrders]
    filterset_class = PurchaseOrderFilter
    search_fields = [
        "po_number",
        "supplier__name",
        "created_by__email",
    ]
    ordering_fields = [
        "po_number",
        "status",
        "order_date",
        "expected_delivery_date",
        "total_amount",
        "created_at",
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        purchase_order = self.get_object()

        if purchase_order.status != PurchaseOrderStatus.DRAFT:
            return Response(
                {"detail": "Only draft purchase orders can be submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not purchase_order.items.exists():
            return Response(
                {"detail": "Cannot submit a purchase order without items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_order.status = PurchaseOrderStatus.SUBMITTED
        purchase_order.submitted_at = timezone.now()
        purchase_order.save(update_fields=["status", "submitted_at", "updated_at"])

        return Response(
            PurchaseOrderSerializer(purchase_order, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanApprovePurchaseOrders],
    )
    def approve(self, request, pk=None):
        purchase_order = self.get_object()

        if purchase_order.status != PurchaseOrderStatus.SUBMITTED:
            return Response(
                {"detail": "Only submitted purchase orders can be approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_order.status = PurchaseOrderStatus.APPROVED
        purchase_order.approved_by = request.user
        purchase_order.approved_at = timezone.now()
        purchase_order.save(
            update_fields=[
                "status",
                "approved_by",
                "approved_at",
                "updated_at",
            ]
        )

        return Response(
            PurchaseOrderSerializer(purchase_order, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanApprovePurchaseOrders],
    )
    def reject(self, request, pk=None):
        purchase_order = self.get_object()

        if purchase_order.status not in [
            PurchaseOrderStatus.DRAFT,
            PurchaseOrderStatus.SUBMITTED,
        ]:
            return Response(
                {"detail": "Only draft or submitted purchase orders can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PurchaseOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        remarks = serializer.validated_data.get("remarks")
        if remarks:
            purchase_order.remarks = remarks

        purchase_order.status = PurchaseOrderStatus.REJECTED
        purchase_order.rejected_at = timezone.now()
        purchase_order.save(update_fields=["status", "remarks", "rejected_at", "updated_at"])

        return Response(
            PurchaseOrderSerializer(purchase_order, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanCompletePurchaseOrders],
    )
    def complete(self, request, pk=None):
        purchase_order = self.get_object()

        if purchase_order.status != PurchaseOrderStatus.APPROVED:
            return Response(
                {"detail": "Only approved purchase orders can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_order.status = PurchaseOrderStatus.COMPLETED
        purchase_order.completed_at = timezone.now()
        purchase_order.save(update_fields=["status", "completed_at", "updated_at"])

        return Response(
            PurchaseOrderSerializer(purchase_order, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )